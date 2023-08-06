#pragma once

#include "tensorflow/core/common_runtime/dml/dml_adapter.h"
#include "tensorflow/core/common_runtime/dml/dml_common.h"

namespace tensorflow {

// Represents a DXCore or DXGI adapter.
class DmlAdapterImpl {
 public:
  /*implicit*/ DmlAdapterImpl(LUID adapterLuid);

#if _WIN32
  /*implicit*/ DmlAdapterImpl(IDXGIAdapter* adapter);
#else
  /*implicit*/ DmlAdapterImpl(IDXCoreAdapter* adapter);
#endif

  IUnknown* Get() const { return adapter_.Get(); }

  DriverVersion DriverVersion() const { return driver_version_; }
  VendorID VendorID() const { return vendor_id_; }
  uint32_t DeviceID() const { return device_id_; }
  const std::string& Name() const { return description_; }
  bool IsComputeOnly() const { return is_compute_only_; }

  uint64_t GetDedicatedMemoryInBytes() const {
    return dedicated_memory_in_bytes_;
  }

 private:
#if _WIN32
  void Initialize(IDXGIAdapter* adapter);
#else
  void Initialize(IDXCoreAdapter* adapter);
#endif

  Microsoft::WRL::ComPtr<IUnknown> adapter_;

  tensorflow::DriverVersion driver_version_;
  tensorflow::VendorID vendor_id_;
  uint32_t device_id_;
  std::string description_;
  bool is_compute_only_;
  uint64_t dedicated_memory_in_bytes_;
};

// Retrieves a list of DML-compatible hardware adapters on the system.
std::vector<DmlAdapterImpl> EnumerateAdapterImpls();

}  // namespace tensorflow