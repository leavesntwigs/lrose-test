#include <limits.h>
#include "gtest/gtest.h"
#include "Solo/SoloFunctions.hh"

namespace {

// Step 2. Use the TEST macro to define your tests.
//
// TEST has two parameters: the test case name and the test name.
// After using the macro, you should define your test logic between a
// pair of braces.  You can use a bunch of macros to indicate the
// success or failure of a test.  EXPECT_TRUE and EXPECT_EQ are
// examples of such macros.  For a complete list, see gtest.h.
//
// <TechnicalDetails>
//
// In Google Test, tests are grouped into test cases.  This is how we
// keep test code organized.  You should put logically related tests
// into the same test case.
//
// The test case name and the test name should both be valid C++
// identifiers.  And you should not use underscore (_) in the names.
//
// Google Test guarantees that each test you define is run exactly
// once, but it makes no guarantee on the order the tests are
// executed.  Therefore, you should write your tests in such a way
// that their results don't depend on their order.
//
// </TechnicalDetails>


// Keep the interface simple
// Inside the C++ code, the structures can be more complicated
//
#define NGATES1 4
  TEST(SoloDespeckle, no_clipping__no_bad_flags__no_boundary) {

    float data[NGATES1] = {3,4,5,6};
    float newData[NGATES1] = {0,0,0,0};
    bool bnd[NGATES1] = {1,1,1,1};
    float bad_flag = -3;
    int a_speckle = 5;

    size_t nGates = NGATES1;
    size_t clip_gate = nGates;
    float newData_expected[NGATES1] = {3, 4, 5, 6};

    se_despeckle(data, newData, nGates, bad_flag, a_speckle, clip_gate, bnd);
    for (int i=0; i<NGATES1; i++)
      EXPECT_EQ(newData[i], newData_expected[i]);
    
  }



}  // namespace

