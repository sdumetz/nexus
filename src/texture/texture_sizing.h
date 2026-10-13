#ifndef NX_TEXTURE_SIZING_H
#define NX_TEXTURE_SIZING_H

#include <algorithm>
#include <utility>

namespace nx {
// Search a proportional sequence of dimensions, rounding both axes upward to
// blocks of four. The footprint evaluator includes chart anisotropy and caps.
template<class Error>
std::pair<int, int> fine_texture_size(int width, int height, double target, Error error) {
	if(target <= 0 || error(width, height) > target) return {width, height};
	// Baked atlases are power-of-two. Preserve unsupported unaligned inputs
	// rather than enlarging them or violating the error constraint.
	if(width % 4 || height % 4) return {width, height};
	const int longest = std::max(width, height);
	auto dimensions = [&](int blocks) {
		auto axis = [&](int size) {
			return std::max(4, 4 * int((static_cast<long long>(size)*blocks + longest-1)/longest));
		};
		return std::make_pair(axis(width), axis(height));
	};
	int low = 1, high = longest/4;
	while(low < high) {
		const int mid = low + (high-low)/2;
		const auto size = dimensions(mid);
		if(error(size.first, size.second) <= target) high = mid;
		else low = mid+1;
	}
	return dimensions(low);
}
}
#endif
