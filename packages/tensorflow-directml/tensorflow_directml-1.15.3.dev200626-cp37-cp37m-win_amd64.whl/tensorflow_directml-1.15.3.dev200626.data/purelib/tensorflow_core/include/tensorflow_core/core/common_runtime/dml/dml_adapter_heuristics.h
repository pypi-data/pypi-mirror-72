#pragma once

namespace tensorflow {

// We don't have an easy way to get detailed architecture-specific information
// from a D3D adapter, so we set these properties to be roughly equivalent to
// an NVIDIA GTX 1070 which we use as the archetype for an "average" GPU.
struct DmlAdapterArchetype {
  // Core clock frequency, in Hz
  static constexpr int64 kFrequency = 1700e6;  // 1700MHz

  // Number of SMs/CUs/EUs
  static constexpr int64 kNumCores = 15;

  // Number of registers per "core" (SM/CU/EU)
  static constexpr int64 kNumRegisters = 65536;

  // Cache sizes, in bytes
  static constexpr int64 kL1CacheSize = 24576;    // 24KB
  static constexpr int64 kL2CacheSize = 2097152;  // 2MB
  static constexpr int64 kL3CacheSize = 0;

  // Shared memory size, in bytes
  static constexpr int64 kSharedMemorySizePerMultiprocessor = 98304;  // 96KB

  // Non-shared dedicated video memory, in bytes
  static constexpr int64 kMemorySize = 8ll << 30;  // 8GB

  // Memory bandwidth, in bytes/s
  static constexpr int64 kBandwidth = 256ll << 30;  // 256GB/s

  // Total compute, in 32-bit floating point operations per second
  static constexpr int64 kComputeFlops = 6.5e12;  // 6.5 TFLOPS
};

}  // namespace tensorflow