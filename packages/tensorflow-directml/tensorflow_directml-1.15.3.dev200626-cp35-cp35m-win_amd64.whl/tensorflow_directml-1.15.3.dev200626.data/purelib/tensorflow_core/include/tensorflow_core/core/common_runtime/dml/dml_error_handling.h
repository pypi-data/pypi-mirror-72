#pragma once

#include "tensorflow/core/platform/default/logging.h"

#define DML_CHECK_SUCCEEDED(hr)      \
  do {                               \
    CHECK_EQ(SUCCEEDED((hr)), true); \
  } while (0)