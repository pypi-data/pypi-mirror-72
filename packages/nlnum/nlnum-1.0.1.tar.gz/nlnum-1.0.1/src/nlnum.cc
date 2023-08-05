// Copyright 2020 ICLUE @ UIUC. All rights reserved.

#include <algorithm>
#include <climits>
#include <cstdint>
#include <exception>
#include <map>
#include <numeric>
#include <vector>

#include <omp.h>

extern "C" {
#include <lrcalc/hashtab.h>
#include <lrcalc/symfcn.h>
#include <lrcalc/vector.h>
}

#include <nlnum/nlnum.h>
#include <nlnum/partitions_in.h>

namespace nlnum {

// Make sure partitions are weakly decreasing and only positive parts.
void ValidatePartitions(const std::vector<Partition>& partitions) {
  for (const Partition& partition : partitions) {
    int last = INT_MAX;
    for (const int part : partition) {
      if (part <= 0) {
        throw std::invalid_argument(
            "The parts of each partition must be positive.");
      }
      if (last < part) {
        throw std::invalid_argument(
            "Each partition must be strictly decreasing.");
      }

      last = part;
    }
  }
}

vector* to_vector(const Partition& vec) {
  vector* v = v_new(static_cast<int>(vec.size()));
  for (size_t i = 0; i < vec.size(); ++i) {
    v->array[i] = vec[i];
  }
  return v;
}

bool to_cppvec(const vector* v, Partition* vec) {
  if (v == nullptr || vec == nullptr) return false;
  vec->clear();

  const size_t n = v->length;
  vec->reserve(n);

  for (size_t i = 0; i < v->length; ++i) {
    vec->push_back(v->array[i]);
  }

  return true;
}

int64_t lrcoef(const Partition& outer, const Partition& inner1,
               const Partition& inner2) {
  ValidatePartitions({outer, inner1, inner2});

  vector* o = to_vector(outer);
  vector* i1 = to_vector(inner1);
  vector* i2 = to_vector(inner2);

  const int64_t result = lrcoef(o, i1, i2);

  v_free(o);
  v_free(i1);
  v_free(i2);

  return result;
}

// Evaluates one term in the sum.
int64_t nlcoef_slow_helper(const Partition& alpha, const Partition& mu,
                           const Partition& nu, const Partition& lambda) {
  int64_t nl_im = 0;

  vector* aa = to_vector(alpha);
  vector* mm = to_vector(mu);
  vector* nn = to_vector(nu);
  hashtab* s1 = skew(mm, aa, 0);
  hashtab* s2 = skew(nn, aa, 0);
  v_free(aa);
  v_free(mm);
  v_free(nn);

  std::map<Partition, int> ss1, ss2;
  to_map(s1, &ss1);
  to_map(s2, &ss2);
  hash_free(s1);
  hash_free(s2);

  for (const auto& p1 : ss1) {
    for (const auto& p2 : ss2) {
      // These are the 2 LR coefficients.
      const int c1 = p1.second;
      const int c2 = p2.second;

      vector* v1 = to_vector(p1.first);
      vector* v2 = to_vector(p2.first);
      hashtab* ht = mult(v1, v2, 0);
      v_free(v1);
      v_free(v2);

      std::map<Partition, int> ss;
      to_map(ht, &ss);
      hash_free(ht);

      if (ss.find(lambda) != ss.end()) {
        const int c3 = ss[lambda];
        nl_im += c1 * c2 * c3;
      }
    }
  }

  return nl_im;
}

// Returns the sum if it is greater than zero, else returns zero.
size_t ZSum(const Partition& parts) {
  return static_cast<size_t>(
      std::max(0, std::accumulate(parts.begin(), parts.end(), 0)));
}

int64_t nlcoef_slow(const Partition& mu, const Partition& nu,
                    const Partition& lambda) {
  ValidatePartitions({mu, nu, lambda});

  int64_t nl = 0;
  // Step 1: Compute the intersection of mu and nu.
  const Partition limit = Intersection(mu, nu);
  const size_t slimit = ZSum(limit);

  // Step 2: Iterate through each partition in the intersection.
  for (size_t size = 0; size <= slimit; ++size) {
    for (const Partition& alpha : PartitionsIn(limit, size)) {
      nl += nlcoef_slow_helper(alpha, mu, nu, lambda);
    }
  }

  return nl;
}

bool to_map(hashtab* ht, std::map<Partition, int>* m) {
  if (ht == nullptr || m == nullptr) return false;
  m->clear();

  hash_itr itr;
  hash_first(ht, itr);
  while (hash_good(itr)) {
    const vector* v = static_cast<vector*>(hash_key(itr));
    Partition p;
    to_cppvec(v, &p);
    const int c = hash_intvalue(itr);
    m->insert({p, c});
    hash_next(itr);
  }

  return true;
}

bool NeedsComputation(const Partition& mu, const Partition& nu,
                      const Partition& lambda, int64_t* nl,
                      std::vector<Partition>* va, std::vector<Partition>* vb,
                      std::vector<Partition>* vc) {
  ValidatePartitions({mu, nu, lambda});
  if (nl == nullptr) return true;

  const Partition int_mn = Intersection(mu, nu);
  const Partition int_ml = Intersection(mu, lambda);
  const Partition int_nl = Intersection(nu, lambda);

  const size_t sl = ZSum(lambda);
  const size_t sm = ZSum(mu);
  const size_t sn = ZSum(nu);

  // Lemma 2.2 (v).
  if ((sl + sm + sn) % 2 == 1) {
    *nl = 0;
    return false;
  }

  // Lemma 2.2 (iii) + some common knowledge.
  if (sl + sm <= sn || sm + sn <= sl || sl + sn <= sm) {
    *nl = 0;
    return false;
  }

  // Lemma 2.2 (ii).
  if (sm + sn == sl) {
    *nl = lrcoef(lambda, mu, nu);
    return false;
  }

  // Lemma 2.2 Equation 6.
  const size_t sa = ((sm + sn) - sl) / 2;
  const size_t sb = ((sl + sm) - sn) / 2;
  const size_t sc = ((sl + sn) - sm) / 2;

  const auto vfn = [&](const PartitionsIn&& pi) {
    std::vector<Partition> v;
    for (const Partition& partition : pi) {
      v.push_back(partition);
    }
    return v;
  };

  if (va == nullptr || vb == nullptr || vc == nullptr) {
    *nl = 0;
    return false;
  }

  *va = vfn(PartitionsIn(int_mn, sa));
  *vb = vfn(PartitionsIn(int_ml, sb));
  *vc = vfn(PartitionsIn(int_nl, sc));

  return true;
}

int64_t nlcoef(const Partition& mu, const Partition& nu,
               const Partition& lambda) {
  int64_t nl;
  std::vector<Partition> va;
  std::vector<Partition> vb;
  std::vector<Partition> vc;
  if (!NeedsComputation(mu, nu, lambda, &nl, &va, &vb, &vc)) return nl;

  nl = 0;
  // The `Release` version seems to benefit from OpenMP parallel directives.
  // Use a `dynamic` schedule since the work is not balanced among iterations.
#pragma omp parallel for reduction(+ : nl) schedule(dynamic)
  for (auto ita = va.begin(); ita < va.end(); ++ita) {
    const Partition& alpha = *ita;
    for (auto itb = vb.begin(); itb < vb.end(); ++itb) {
      const Partition& beta = *itb;
      const int64_t cabm = lrcoef(mu, alpha, beta);
      if (cabm == 0) continue;
      for (auto itc = vc.begin(); itc < vc.end(); ++itc) {
        const Partition& gamma = *itc;

        const int64_t cacn = lrcoef(nu, alpha, gamma);
        if (cacn == 0) continue;
        const int64_t cbcl = lrcoef(lambda, beta, gamma);
        if (cbcl == 0) continue;

        nl += cabm * cacn * cbcl;
      }
    }
  }

  return nl;
}

}  // namespace nlnum

