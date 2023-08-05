// Copyright (c) 2020 ICLUE @ UIUC. All rights reserved.

#ifndef NLNUM_PARTITIONS_IN_H_
#define NLNUM_PARTITIONS_IN_H_

#include <iterator>
#include <vector>

namespace nlnum {

typedef std::vector<int> Partition;

// Iterates through each partition contained within a given partition `limit`.
class PartitionsIn {
 public:
  PartitionsIn(const Partition& limit, const size_t size);

  class const_iterator : public std::iterator<std::forward_iterator_tag, Partition> {
   public:
    const_iterator(const Partition& limit, const size_t size);
    const_iterator& operator++();
    const Partition& operator*() const;
    bool operator!=(const const_iterator&) const;

   private:
    struct var {
      size_t level;
      int rem;
      int mn;
      int mx;
      var* came_from;

      var(size_t level, int rem, int mn, int mx, var* came_from)
          : level(level), rem(rem), mn(mn), mx(mx), came_from(came_from) {}
    };

    bool Next();
    bool GoBack(var* v);

   private:
    const Partition limit_;
    const size_t size_;
    Partition parts_;
    Partition ret_parts_;
    std::vector<int> rsums_;
    std::vector<var*> call_stack_;
    bool done_;
  };

 public:
  const_iterator begin() const;
  const_iterator end() const;

 private:
  const size_t size_;
  const Partition limit_;
};

// Computes the intersection of two partitions.
const std::vector<int> Intersection(const Partition&, const Partition&);

}  // namespace nlnum

#endif  // NLNUM_PARTITIONS_IN_H_
