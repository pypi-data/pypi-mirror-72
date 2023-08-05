
#include <algorithm>
#include <iterator>
#include <stdexcept>
#include <bitset>
#include <cmath>
#include <cassert>
#include <cstring>

#include "zstd.h"
#include <zlib.h>

#include "genotypes.h"
#include "utils.h"

namespace bgen {

void zlib_uncompress(char * input, int compressed_len, char * decompressed, int decompressed_len) {
  /* uncompress a char array with zlib
  */
  z_stream infstream;
  infstream.zalloc = Z_NULL;
  infstream.zfree = Z_NULL;
  infstream.opaque = Z_NULL;
  
  infstream.avail_in = compressed_len; // size of input
  infstream.next_in = (Bytef *) input; // input char array
  infstream.avail_out = decompressed_len; // size of output
  infstream.next_out = (Bytef *) decompressed; // output char array
  
  inflateInit(&infstream);
  inflate(&infstream, Z_NO_FLUSH);
  inflateEnd(&infstream);
  
  if (decompressed_len != (int) infstream.total_out) {
    throw std::invalid_argument("zlib decompression gave data of wrong length");
  }
}

void zstd_uncompress(char * input, int compressed_len, char * decompressed,  int decompressed_len) {
  /* uncompress a char array with zstd
  */
  std::size_t total_out = ZSTD_decompress(decompressed, decompressed_len, input, compressed_len);
  if (decompressed_len != (int) total_out) {
    throw std::invalid_argument("zstd decompression gave data of wrong length");
  }
}

void Genotypes::decompress(char * bytes, int compressed_len, char * decompressed, int decompressed_len) {
  /* decompress the probabilty data
  */
  switch (compression) {
    case 0: { // no compression
      decompressed = bytes;
      break;
    }
    case 1: { // zlib
      zlib_uncompress(bytes, compressed_len, decompressed, decompressed_len);
      break;
    }
    case 2: { //zstd
      zstd_uncompress(bytes, compressed_len, decompressed, decompressed_len);
      break;
    }
  }
}

uint get_max_probs(int max_ploidy, int n_alleles, bool phased) {
  // figure out the maximum number of probabilities across the individuals
  uint max_probs;
  if (phased) {
    max_probs = n_alleles;
  } else {
    max_probs = n_choose_k(max_ploidy + n_alleles - 1, n_alleles - 1);
  }
  return max_probs;
}

void Genotypes::parse_ploidy(char * uncompressed, uint & idx) {
  // get ploidy and missingness for layout2. this uses 3 milliseconds for 500k samples
  
  ploidy = new std::uint8_t[n_samples];
  
  // we want to avoid parsing the ploidy states if  every sample has the same
  // ploidy. If we have a constant ploidy, set all entries to the same value
  std::uint8_t mask = 63;
  if (constant_ploidy) {
    std::memset(ploidy, max_ploidy, n_samples);
    for (uint x=0; x < n_samples; x++) {
      if (uncompressed[idx + x] & 0x80) {
        missing.push_back(x);
      }
    }
  } else {
    for (uint x=0; x < n_samples; x++) {
      ploidy[x] = mask & uncompressed[idx + x];
      if (uncompressed[idx + x] & 0x80) {
        missing.push_back(x);
      }
    }
  }
  idx += n_samples;
}

float * Genotypes::parse_layout1(char * uncompressed) {
  /* parse probabilities for layout1
  */
  phased = false;
  min_ploidy = 2;
  max_ploidy = 2;
  constant_ploidy = (min_ploidy == max_ploidy);
  ploidy = new std::uint8_t[n_samples];
  max_probs = get_max_probs(max_ploidy, n_alleles, phased);
  probs = new float[max_probs * n_samples];
  
  uint idx = 0;
  uint bit_len = 2;
  float factor = 1.0 / 32768;
  float prob;
  uint offset;
  for (uint n=0; n<n_samples; n++) {
    offset = max_probs * n;
    for (int x=0; x<3; x++) {
      prob = (float) *reinterpret_cast<const std::uint16_t*>(&uncompressed[idx]) * factor;
      probs[offset + x] = prob;
      idx += bit_len;
    }
    if ((probs[offset] == 0.0) & (probs[offset + 1] == 0.0) & (probs[offset + 2] == 0.0)) {
      probs[offset] = std::nan("1");
      probs[offset + 1] = std::nan("1");
      probs[offset + 2] = std::nan("1");
    }
  }
  return probs;
}

float * Genotypes::parse_layout2(char * uncompressed) {
  /* parse probabilities for layout2
  */
  uint idx = 0;
  std::uint32_t nn_samples = *reinterpret_cast<const std::uint32_t*>(&uncompressed[idx]);
  idx += sizeof(std::uint32_t);
  std::uint16_t allele_check = *reinterpret_cast<const std::uint16_t*>(&uncompressed[idx]);
  idx += sizeof(std::uint16_t);
  if (nn_samples != (std::uint32_t) n_samples) {
    throw std::invalid_argument("number of samples doesn't match!");
  }
  if (allele_check != n_alleles) {
    throw std::invalid_argument("number of alleles doesn't match!");
  }
  
  min_ploidy = (int) *reinterpret_cast<const std::uint8_t*>(&uncompressed[idx]);
  idx += sizeof(std::uint8_t);
  max_ploidy = (int) *reinterpret_cast<const std::uint8_t*>(&uncompressed[idx]);
  idx += sizeof(std::uint8_t);
  
  constant_ploidy = (min_ploidy == max_ploidy);
  parse_ploidy(uncompressed, idx);
  
  phased = (bool) *reinterpret_cast<const std::uint8_t*>(&uncompressed[idx]);
  idx += sizeof(std::uint8_t);
  uint bit_depth = (int) *reinterpret_cast<const std::uint8_t*>(&uncompressed[idx]);
  if ((bit_depth < 1) | (bit_depth > 32)) {
    throw std::invalid_argument("probabilities bit depth out of bounds");
  }
  
  idx += sizeof(std::uint8_t);
  float factor = 1.0 / ((float) (std::pow(2, (int) bit_depth)) - 1);
  
  max_probs = get_max_probs(max_ploidy, n_alleles, phased);
  uint nrows = 0;
  if (!phased) {
    nrows = n_samples;
  } else {
    // phased probabilities require as many rows per sample as the ploidy
    if (constant_ploidy) {
      nrows = n_samples * max_ploidy;
    } else {
      for (uint n=0; n<n_samples; n++) { nrows += ploidy[n]; }
    }
  }
  probs = new float[max_probs * nrows];
  
  // get genotype/allele probabilities
  uint n_probs;
  uint max_less_1 = max_probs - 1;
  float prob = 0;
  float remainder;
  
  // define variables for parsing depths not aligned with 8 bit char array
  std::uint64_t probs_mask = std::uint64_t(0xFFFFFFFFFFFFFFFF) >> (64 - bit_depth);
  uint bit_idx = 0;  // index position in bits
  
  for (uint offset=0; offset < (nrows * max_probs); offset += max_probs) {
    // calculate the number of probabilities per sample (depends on whether the
    // data is phased, the sample ploidy and the number of alleles)
    if (constant_ploidy) {
      n_probs = max_less_1;
    } else if (phased) {
      n_probs = n_alleles - 1;
    } else if ((ploidy[offset / max_probs] == 2) && (n_alleles == 2)) {
      n_probs = 2;
    } else {
      n_probs = n_choose_k(ploidy[offset / max_probs] + n_alleles - 1, n_alleles - 1) - 1;
    }
    remainder = 1.0;
    for (uint x=0; x<n_probs; x++) {
      prob = ((*reinterpret_cast<const std::uint64_t* >(&uncompressed[idx + bit_idx / 8]) >> bit_idx % 8) & probs_mask) * factor ;
      bit_idx += bit_depth;
      remainder -= prob;
      probs[offset + x] = prob;
    }
    probs[offset + n_probs] = remainder;
    for (uint x=(n_probs + 1); x<max_probs; x++) {
      probs[offset + x] = std::nan("1");
    }
  }
  
  uint offset;
  // for samples with missing data, just set values to NA
  for (auto n: missing) {
    offset = max_probs * n;
    for (uint x=0; x<max_probs; x++) {
      probs[offset + x] = std::nan("1");
    }
  }
  return probs;
}

float * Genotypes::probabilities() {
  /* parse genotype data for a single variant
  */
  // avoid recomputation if called repeatedly for same variant
  if (max_probs > 0) {
    return probs;
  }
  
  handle->seekg(offset);  // about 1 microsecond
  
  bool decompressed_field = false;
  std::uint32_t decompressed_len = 0;
  if (compression != 0) {
    if (layout == 1) {
      decompressed_len = n_samples * 6;
    } else if (layout == 2) {
      decompressed_field = true;
      handle->read(reinterpret_cast<char*>(&decompressed_len), sizeof(std::uint32_t));
    }
  }
  
  std::uint32_t compressed_len = next_var_offset - offset - decompressed_field * 4;
  char geno[compressed_len];
  char uncompressed[decompressed_len];
  handle->read(&geno[0], compressed_len); // about 20 microseconds
  decompress(geno, (int) compressed_len, uncompressed, (int) decompressed_len);  // about 2 milliseconds
  
  switch (layout) {
    case 1: {
      probs = parse_layout1(uncompressed);
      break;
    }
    case 2: {
      probs = parse_layout2(uncompressed);  // about 3 milliseconds
      break;
    }
  }
  return probs;
}

void Genotypes::clear_probs() {
  if (max_probs > 0) {
    delete[] probs;
    delete[] ploidy;
    missing.clear();
  }
  max_probs = 0;
}

} //namespace bgen
