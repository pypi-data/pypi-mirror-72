#include "cloud.h"
#include "nanoflann.hpp"
#include <cstdint>
#include <iostream>
#include <set>
#include <thread>

typedef struct thread_struct {
  void *kd_tree;
  void *matches;
  void *queries;
  size_t *max_count;
  std::mutex *ct_m;
  std::mutex *tree_m;
  size_t start;
  size_t end;
  double search_radius;
  bool small;
  bool option;
  size_t k;
} thread_args;

template <typename scalar_t> void thread_routine(thread_args *targs) {
  typedef nanoflann::KDTreeSingleIndexAdaptor<
      nanoflann::L2_Adaptor<scalar_t, PointCloud<scalar_t>>,
      PointCloud<scalar_t>>
      my_kd_tree_t;
  typedef std::vector<std::vector<std::pair<size_t, scalar_t>>> kd_pair;
  my_kd_tree_t *index = (my_kd_tree_t *)targs->kd_tree;
  kd_pair *matches = (kd_pair *)targs->matches;
  PointCloud<scalar_t> *pcd_query = (PointCloud<scalar_t> *)targs->queries;
  size_t *max_count = targs->max_count;
  std::mutex *ct_m = targs->ct_m;
  std::mutex *tree_m = targs->tree_m;
  double eps;
  if (targs->small) {
    eps = 0.000001;
  } else {
    eps = 0;
  }
  double search_radius = (double)targs->search_radius;
  size_t start = targs->start;
  size_t end = targs->end;
  auto k = targs->k;
  for (size_t i = start; i < end; i++) {

    std::vector<scalar_t> p0 = *(((*pcd_query).pts)[i]);

    scalar_t *query_pt = new scalar_t[p0.size()];
    std::copy(p0.begin(), p0.end(), query_pt);
    (*matches)[i].reserve(*max_count);
    std::vector<std::pair<size_t, scalar_t>> ret_matches;
    std::vector<size_t> *knn_ret_matches = new std::vector<size_t>(k);
    std::vector<scalar_t> *knn_dist_matches = new std::vector<scalar_t>(k);

    tree_m->lock();

    size_t nMatches;
    if (targs->option) {
      nMatches = index->radiusSearch(query_pt, (scalar_t)(search_radius + eps),
                                     ret_matches, nanoflann::SearchParams());
    } else {
      nMatches = index->knnSearch(query_pt, k, &(*knn_ret_matches)[0],
                                  &(*knn_dist_matches)[0]);
      auto temp = new std::vector<std::pair<size_t, scalar_t>>(
          (*knn_dist_matches).size());
      for (size_t j = 0; j < (*knn_ret_matches).size(); j++) {
        (*temp)[j] =
            std::make_pair((*knn_ret_matches)[j], (*knn_dist_matches)[j]);
      }
      ret_matches = *temp;
    }
    tree_m->unlock();

    (*matches)[i] = ret_matches;

    ct_m->lock();
    if (*max_count < nMatches) {
      *max_count = nMatches;
    }
    ct_m->unlock();
  }
}

template <typename scalar_t>
size_t nanoflann_neighbors(std::vector<scalar_t> &queries,
                           std::vector<scalar_t> &supports,
                           std::vector<size_t> *&neighbors_indices,
                           double radius, int dim, int64_t max_num,
                           int64_t n_threads, int64_t k, int option) {

  const scalar_t search_radius = static_cast<scalar_t>(radius * radius);

  // Counting vector
  size_t *max_count = new size_t();
  *max_count = 1;

  size_t ssize = supports.size();
  // CLoud variable
  PointCloud<scalar_t> pcd;
  pcd.set(supports, dim);
  // Cloud query
  PointCloud<scalar_t> *pcd_query = new PointCloud<scalar_t>();
  (*pcd_query).set(queries, dim);

  // Tree parameters
  nanoflann::KDTreeSingleIndexAdaptorParams tree_params(15 /* max leaf */);

  // KDTree type definition
  typedef nanoflann::KDTreeSingleIndexAdaptor<
      nanoflann::L2_Adaptor<scalar_t, PointCloud<scalar_t>>,
      PointCloud<scalar_t>>
      my_kd_tree_t;
  typedef std::vector<std::vector<std::pair<size_t, scalar_t>>> kd_pair;

  // Pointer to trees
  my_kd_tree_t *index;
  index = new my_kd_tree_t(dim, pcd, tree_params);
  index->buildIndex();
  // Search neigbors indices

  // Search params
  nanoflann::SearchParams search_params;
  // search_params.sorted = true;
  kd_pair *list_matches = new kd_pair((*pcd_query).pts.size());

  // single threaded routine
  if (n_threads == 1) {
    size_t i0 = 0;
    double eps;
    if (ssize < 10) {
      eps = 0.000001;
    } else {
      eps = 0;
    }

    for (auto &p : (*pcd_query).pts) {
      auto p0 = *p;
      // Find neighbors
      scalar_t *query_pt = new scalar_t[dim];
      std::copy(p0.begin(), p0.end(), query_pt);

      (*list_matches)[i0].reserve(*max_count);
      std::vector<std::pair<size_t, scalar_t>> ret_matches;
      std::vector<size_t> *knn_ret_matches = new std::vector<size_t>(k);
      std::vector<scalar_t> *knn_dist_matches = new std::vector<scalar_t>(k);

      size_t nMatches;
      if (!!(option)) {
        nMatches =
            index->radiusSearch(query_pt, (scalar_t)(search_radius + eps),
                                ret_matches, search_params);
      } else {
        nMatches = index->knnSearch(query_pt, (size_t)k, &(*knn_ret_matches)[0],
                                    &(*knn_dist_matches)[0]);
        auto temp = new std::vector<std::pair<size_t, scalar_t>>(
            (*knn_dist_matches).size());
        for (size_t j = 0; j < (*knn_ret_matches).size(); j++) {
          (*temp)[j] =
              std::make_pair((*knn_ret_matches)[j], (*knn_dist_matches)[j]);
        }
        ret_matches = *temp;
      }
      (*list_matches)[i0] = ret_matches;
      if (*max_count < nMatches)
        *max_count = nMatches;
      i0++;
    }
  } else { // Multi-threaded routine
    std::mutex *mtx = new std::mutex();
    std::mutex *mtx_tree = new std::mutex();

    size_t n_queries = (*pcd_query).pts.size();
    size_t actual_threads =
        std::min((long long)n_threads, (long long)n_queries);

    std::vector<std::thread *> tid(actual_threads);

    size_t start, end;
    size_t length;
    if (n_queries) {
      length = 1;
    } else {
      auto res = std::lldiv((long long)n_queries, (long long)n_threads);
      length = (size_t)res.quot;
    }
    for (size_t t = 0; t < actual_threads; t++) {
      start = t * length;
      if (t == actual_threads - 1) {
        end = n_queries;
      } else {
        end = (t + 1) * length;
      }
      thread_args *targs = new thread_args();
      targs->kd_tree = index;
      targs->matches = list_matches;
      targs->max_count = max_count;
      targs->ct_m = mtx;
      targs->tree_m = mtx_tree;
      targs->search_radius = search_radius;
      targs->queries = pcd_query;
      targs->start = start;
      targs->end = end;
      if (ssize < 10) {
        targs->small = true;
      } else {
        targs->small = false;
      }
      targs->option = !!(option);
      targs->k = k;
      std::thread *temp = new std::thread(thread_routine<scalar_t>, targs);
      tid[t] = temp;
    }

    for (size_t t = 0; t < actual_threads; t++) {
      tid[t]->join();
    }
  }

  // Reserve the memory
  if (max_num > 0) {
    *max_count = max_num;
  }

  size_t size = 0; // total number of edges
  for (auto &inds : *list_matches) {
    if (inds.size() <= *max_count)
      size += inds.size();
    else
      size += *max_count;
  }

  neighbors_indices->resize(size * 2);
  size_t i1 = 0; // index of the query points
  size_t u = 0;  // curent index of the neighbors_indices
  for (auto &inds : *list_matches) {
    for (size_t j = 0; j < *max_count; j++) {
      if (j < inds.size()) {
        (*neighbors_indices)[u] = inds[j].first;
        (*neighbors_indices)[u + 1] = i1;
        u += 2;
      }
    }
    i1++;
  }

  return *max_count;
}

template <typename scalar_t>
size_t batch_nanoflann_neighbors(std::vector<scalar_t> &queries,
                                 std::vector<scalar_t> &supports,
                                 std::vector<long> &q_batches,
                                 std::vector<long> &s_batches,
                                 std::vector<size_t> *&neighbors_indices,
                                 double radius, int dim, int64_t max_num,
                                 int64_t k, int option) {

  // Indices.
  size_t i0 = 0;

  // Square radius.
  const scalar_t r2 = static_cast<scalar_t>(radius * radius);

  // Counting vector.
  size_t max_count = 0;

  // Batch index.
  size_t b = 0;
  size_t sum_qb = 0;
  size_t sum_sb = 0;

  double eps;
  if (supports.size() < 10) {
    eps = 0.000001;
  } else {
    eps = 0;
  }
  // Nanoflann related variables.

  // Cloud variable.
  PointCloud<scalar_t> current_cloud;
  PointCloud<scalar_t> query_pcd;
  query_pcd.set(queries, dim);
  std::vector<std::vector<std::pair<size_t, scalar_t>>> all_inds_dists(
      query_pcd.pts.size());

  // Tree parameters.
  nanoflann::KDTreeSingleIndexAdaptorParams tree_params(10 /* max leaf */);

  // KDTree type definition.
  typedef nanoflann::KDTreeSingleIndexAdaptor<
      nanoflann::L2_Adaptor<scalar_t, PointCloud<scalar_t>>,
      PointCloud<scalar_t>>
      my_kd_tree_t;

  // Pointer to trees.
  my_kd_tree_t *index;
  // Build KDTree for the first batch element.
  current_cloud.set_batch(supports, sum_sb, s_batches[b], dim);
  index = new my_kd_tree_t(dim, current_cloud, tree_params);
  index->buildIndex();
  // Search neigbors indices.
  // Search params.
  nanoflann::SearchParams search_params;
  search_params.sorted = true;

  for (auto &p : query_pcd.pts) {
    auto p0 = *p;
    // Check if we changed batch.

    scalar_t *query_pt = new scalar_t[dim];
    std::copy(p0.begin(), p0.end(), query_pt);

    if (i0 == sum_qb + q_batches[b]) {
      sum_qb += q_batches[b];
      sum_sb += s_batches[b];
      b++;

      // Change the points.
      current_cloud.pts.clear();
      current_cloud.set_batch(supports, sum_sb, s_batches[b], dim);
      // Build KDTree of the current element of the batch.
      delete index;
      index = new my_kd_tree_t(dim, current_cloud, tree_params);
      index->buildIndex();
    }
    // Initial guess of neighbors size.
    all_inds_dists[i0].reserve(max_count);

    // Find neighbors.
    size_t nMatches;
    if (!!option) {
      nMatches = index->radiusSearch(query_pt, r2 + eps, all_inds_dists[i0],
                                     search_params);
      // Update max count.
    } else {
      std::vector<size_t> *knn_ret_matches = new std::vector<size_t>(k);
      std::vector<scalar_t> *knn_dist_matches = new std::vector<scalar_t>(k);
      nMatches = index->knnSearch(query_pt, (size_t)k, &(*knn_ret_matches)[0],
                                  &(*knn_dist_matches)[0]);
      auto temp = new std::vector<std::pair<size_t, scalar_t>>(
          (*knn_dist_matches).size());
      for (size_t j = 0; j < (*knn_ret_matches).size(); j++) {
        (*temp)[j] =
            std::make_pair((*knn_ret_matches)[j], (*knn_dist_matches)[j]);
      }
      all_inds_dists[i0] = *temp;
    }
    if (nMatches > max_count)
      max_count = nMatches;
    i0++;
  }

  // How many neighbors do we keep.
  if (max_num > 0) {
    max_count = max_num;
  }

  size_t size = 0; // Total number of edges.
  for (auto &inds_dists : all_inds_dists) {
    if (inds_dists.size() <= max_count)
      size += inds_dists.size();
    else
      size += max_count;
  }

  neighbors_indices->resize(size * 2);
  i0 = 0;
  sum_sb = 0;
  sum_qb = 0;
  b = 0;
  size_t u = 0;
  for (auto &inds_dists : all_inds_dists) {
    if (i0 == sum_qb + q_batches[b]) {
      sum_qb += q_batches[b];
      sum_sb += s_batches[b];
      b++;
    }
    for (size_t j = 0; j < max_count; j++) {
      if (j < inds_dists.size()) {
        (*neighbors_indices)[u] = inds_dists[j].first + sum_sb;
        (*neighbors_indices)[u + 1] = i0;
        u += 2;
      }
    }
    i0++;
  }

  return max_count;
}
