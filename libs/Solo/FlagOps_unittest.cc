#include <limits.h>
#include <math.h>
#include <vector>
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

#define NGATES_4 4
  
  TEST(FlagOps, set_bad_flags_where_below) {
    float data[NGATES_4] = {3,4,5,-6};
    bool bnd[NGATES_4] = {true, true, true, true};
    float bad_flag = -3;

    size_t nGates = NGATES_4;
    size_t clip_gate = nGates;
    bool bad_flag_mask[NGATES_4] = {false, false, false, false};

    bool bad_flag_mask_expected[NGATES_4] = {true, false, false, true};

    char where[] = "below";
    float scaled_thr1 = 4;
    float scaled_thr2 = 0;

    se_set_bad_flags(where, scaled_thr1, scaled_thr2, data, nGates,
		     bad_flag, clip_gate, bnd, bad_flag_mask);

    for (int i=0; i<NGATES_4; i++)
      EXPECT_EQ(bad_flag_mask[i], bad_flag_mask_expected[i]);
  }

  TEST(FlagOps, set_bad_flags_where_below_with_boundary) {
    float data[NGATES_4] = {3,4,5,-6};
    bool bnd[NGATES_4] = {false, false, true, true};
    float bad_flag = -3;

    size_t nGates = NGATES_4;
    size_t clip_gate = nGates;
    bool bad_flag_mask[NGATES_4] = {false, true, false, false};

    bool bad_flag_mask_expected[NGATES_4] = {false, false, false, true};

    char where[] = "below";
    float scaled_thr1 = 4;
    float scaled_thr2 = 0;

    se_set_bad_flags(where, scaled_thr1, scaled_thr2, data, nGates,
		     bad_flag, clip_gate, bnd, bad_flag_mask);

    for (int i=0; i<NGATES_4; i++) {
      //printf("i=%d\n", i);
      EXPECT_EQ(bad_flag_mask[i], bad_flag_mask_expected[i]);
    }
  }

  TEST(FlagOps, set_bad_flags_where_below_with_bad_data) {
    float data[NGATES_4] = {3,-3,5,-6};
    bool bnd[NGATES_4] = {true, true, true, true};
    float bad_flag = -3;

    size_t nGates = NGATES_4;
    size_t clip_gate = nGates;
    bool bad_flag_mask[NGATES_4] = {false, true, false, false};

    bool bad_flag_mask_expected[NGATES_4] = {true, false, false, true};

    char where[] = "below";
    float scaled_thr1 = 4;
    float scaled_thr2 = 0;

    se_set_bad_flags(where, scaled_thr1, scaled_thr2, data, nGates,
		     bad_flag, clip_gate, bnd, bad_flag_mask);

    for (int i=0; i<NGATES_4; i++) {
      //printf("i=%d\n", i);
      EXPECT_EQ(bad_flag_mask[i], bad_flag_mask_expected[i]);
    }
  }

  TEST(FlagOps, set_bad_flags_where_below_with_clip_gate) {
    float data[NGATES_4] = {3,4,5,-6};
    bool bnd[NGATES_4] = {true, true, true, true};
    float bad_flag = -3;

    size_t nGates = NGATES_4;
    size_t clip_gate = nGates-2;
    bool bad_flag_mask[NGATES_4] = {false, true, false, false};

    bool bad_flag_mask_expected[NGATES_4] = {true, false, false, false};

    char where[] = "below";
    float scaled_thr1 = 4;
    float scaled_thr2 = 0;

    se_set_bad_flags(where, scaled_thr1, scaled_thr2, data, nGates,
		     bad_flag, clip_gate, bnd, bad_flag_mask);

    for (int i=0; i<NGATES_4; i++)
      EXPECT_EQ(bad_flag_mask[i], bad_flag_mask_expected[i]);
  }

  
  TEST(FlagOps, set_bad_flags_where_above) {
    float data[NGATES_4] = {-8,4,5,6};
    bool bnd[NGATES_4] = {true, true, true, true};
    float bad_flag = -3;

    size_t nGates = NGATES_4;
    size_t clip_gate = nGates;
    bool bad_flag_mask[NGATES_4] = {false, false, false, false};

    bool bad_flag_mask_expected[NGATES_4] = {false, false, true, true};

    char where[] = "above";
    float scaled_thr1 = 4;
    float scaled_thr2 = 0;

    se_set_bad_flags(where, scaled_thr1, scaled_thr2, data, nGates,
		     bad_flag, clip_gate, bnd, bad_flag_mask);

    for (int i=0; i<NGATES_4; i++)
      EXPECT_EQ(bad_flag_mask[i], bad_flag_mask_expected[i]);
  }

  TEST(FlagOps, set_bad_flags_where_above_with_boundary) {
    float data[NGATES_4] = {3,4,5,-6};
    bool bnd[NGATES_4] = {true, false, true, true};
    float bad_flag = -3;

    size_t nGates = NGATES_4;
    size_t clip_gate = nGates;
    bool bad_flag_mask[NGATES_4] = {false, false, true, false};

    bool bad_flag_mask_expected[NGATES_4] = {false, false, true, false};

    char where[] = "above";
    float scaled_thr1 = 4;
    float scaled_thr2 = 0;

    se_set_bad_flags(where, scaled_thr1, scaled_thr2, data, nGates,
		     bad_flag, clip_gate, bnd, bad_flag_mask);

    for (int i=0; i<NGATES_4; i++) {
      //printf("i=%d\n", i);
      EXPECT_EQ(bad_flag_mask[i], bad_flag_mask_expected[i]);
    }
  }

  TEST(FlagOps, set_bad_flags_where_above_with_bad_data) {
    float data[NGATES_4] = {6,-3,5,6};
    bool bnd[NGATES_4] = {true, true, true, true};
    float bad_flag = -3;

    size_t nGates = NGATES_4;
    size_t clip_gate = nGates;
    bool bad_flag_mask[NGATES_4] = {false, true, false, false};

    bool bad_flag_mask_expected[NGATES_4] = {true, false, true, true};

    char where[] = "above";
    float scaled_thr1 = 4;
    float scaled_thr2 = 0;

    se_set_bad_flags(where, scaled_thr1, scaled_thr2, data, nGates,
		     bad_flag, clip_gate, bnd, bad_flag_mask);

    for (int i=0; i<NGATES_4; i++) {
      //printf("i=%d\n", i);
      EXPECT_EQ(bad_flag_mask[i], bad_flag_mask_expected[i]);
    }
  }

  TEST(FlagOps, set_bad_flags_where_above_with_clip_gate) {
    float data[NGATES_4] = {3,4,5,-6};
    bool bnd[NGATES_4] = {true, true, true, true};
    float bad_flag = -3;

    size_t nGates = NGATES_4;
    size_t clip_gate = nGates-2;
    bool bad_flag_mask[NGATES_4] = {false, true, false, false};

    bool bad_flag_mask_expected[NGATES_4] = {false, false, true, false};

    char where[] = "above";
    float scaled_thr1 = 4;
    float scaled_thr2 = 0;

    se_set_bad_flags(where, scaled_thr1, scaled_thr2, data, nGates,
		     bad_flag, clip_gate, bnd, bad_flag_mask);

    for (int i=0; i<NGATES_4; i++)
      EXPECT_EQ(bad_flag_mask[i], bad_flag_mask_expected[i]);
  }

  
  TEST(FlagOps, set_bad_flags_where_between) {
    float data[NGATES_4] = {-8,4,5,6};
    bool bnd[NGATES_4] = {true, true, true, true};
    float bad_flag = -3;

    size_t nGates = NGATES_4;
    size_t clip_gate = nGates;
    bool bad_flag_mask[NGATES_4] = {false, false, false, false};

    bool bad_flag_mask_expected[NGATES_4] = {false, true, true, false};

    char where[] = "between";
    float scaled_thr1 = 0;
    float scaled_thr2 = 5;

    se_set_bad_flags(where, scaled_thr1, scaled_thr2, data, nGates,
		     bad_flag, clip_gate, bnd, bad_flag_mask);

    for (int i=0; i<NGATES_4; i++)
      EXPECT_EQ(bad_flag_mask[i], bad_flag_mask_expected[i]);
  }

  TEST(FlagOps, set_bad_flags_where_between_with_boundary) {
    float data[NGATES_4] = {3,4,5,-6};
    bool bnd[NGATES_4] = {true, false, true, true};
    float bad_flag = -3;

    size_t nGates = NGATES_4;
    size_t clip_gate = nGates;
    bool bad_flag_mask[NGATES_4] = {false, false, true, false};

    bool bad_flag_mask_expected[NGATES_4] = {false, false, false, true};

    char where[] = "between";
    float scaled_thr1 = -14;
    float scaled_thr2 = 0;

    se_set_bad_flags(where, scaled_thr1, scaled_thr2, data, nGates,
		     bad_flag, clip_gate, bnd, bad_flag_mask);

    for (int i=0; i<NGATES_4; i++) {
      //printf("i=%d\n", i);
      EXPECT_EQ(bad_flag_mask[i], bad_flag_mask_expected[i]);
    }
  }

  TEST(FlagOps, set_bad_flags_where_between_with_bad_data) {
    float data[NGATES_4] = {-6,-3,5,0};
    bool bnd[NGATES_4] = {true, true, true, true};
    float bad_flag = -3;

    size_t nGates = NGATES_4;
    size_t clip_gate = nGates;
    bool bad_flag_mask[NGATES_4] = {false, true, false, false};

    bool bad_flag_mask_expected[NGATES_4] = {true, false, false, true};

    char where[] = "between";
    float scaled_thr1 = -14;
    float scaled_thr2 = 0;

    se_set_bad_flags(where, scaled_thr1, scaled_thr2, data, nGates,
		     bad_flag, clip_gate, bnd, bad_flag_mask);

    for (int i=0; i<NGATES_4; i++) {
      //printf("i=%d\n", i);
      EXPECT_EQ(bad_flag_mask[i], bad_flag_mask_expected[i]);
    }
  }

  TEST(FlagOps, set_bad_flags_where_between_with_clip_gate) {
    float data[NGATES_4] = {3,-4,5,-6};
    bool bnd[NGATES_4] = {true, true, true, true};
    float bad_flag = -3;

    size_t nGates = NGATES_4;
    size_t clip_gate = nGates-2;
    bool bad_flag_mask[NGATES_4] = {false, true, false, false};

    bool bad_flag_mask_expected[NGATES_4] = {true, true, true, false};

    char where[] = "between";
    float scaled_thr1 = -4;
    float scaled_thr2 = 5;

    se_set_bad_flags(where, scaled_thr1, scaled_thr2, data, nGates,
		     bad_flag, clip_gate, bnd, bad_flag_mask);

    for (int i=0; i<NGATES_4; i++)
      EXPECT_EQ(bad_flag_mask[i], bad_flag_mask_expected[i]);
  }

  //
  // assert_bad_flags  
  //

  TEST(FlagOps, assert_bad_flags) {
    float data[NGATES_4] = {3,4,5,-6};
    bool bnd[NGATES_4] = {true, true, true, true};
    float bad_flag = -3;

    size_t nGates = NGATES_4;
    size_t clip_gate = nGates;
    bool bad_flag_mask[NGATES_4] = {true, false, false, true};

    float newData[NGATES_4] =         {0,0,0,0};
    float newDataExpected[NGATES_4] = {-3,4,5,-3};

    se_assert_bad_flags(data, newData, nGates,
		     bad_flag, clip_gate, bnd, bad_flag_mask);

    for (int i=0; i<NGATES_4; i++)
      EXPECT_EQ(newData[i], newDataExpected[i]);
  }

  TEST(FlagOps, assert_bad_flags_with_boundary) {
    float data[NGATES_4] = {3,4,5,-6};
    bool bnd[NGATES_4] = {false, false, true, true};
    float bad_flag = -3;

    size_t nGates = NGATES_4;
    size_t clip_gate = nGates;
    bool bad_flag_mask[NGATES_4] = {false, true, true, true};

    float newData[NGATES_4] =         {0,0,0,0};
    float newDataExpected[NGATES_4] = {3,4,-3,-3};

    se_assert_bad_flags(data, newData, nGates,
		     bad_flag, clip_gate, bnd, bad_flag_mask);

    for (int i=0; i<NGATES_4; i++) {
      //printf("i=%d\n", i);
      EXPECT_EQ(newData[i], newDataExpected[i]);
    }
  }

  TEST(FlagOps, assert_bad_flags_with_clip_gate_negative) {
    float data[NGATES_4] = {3,-3,5,-6};
    bool bnd[NGATES_4] = {true, true, true, true};
    float bad_flag = -3;

    size_t nGates = NGATES_4;
    size_t clip_gate = -3;
    bool bad_flag_mask[NGATES_4] = {false, true, false, false};

    float newData[NGATES_4] =         {0,0,0,0};
    float newDataExpected[NGATES_4] = {3,-3,5,-6};

    se_assert_bad_flags(data, newData, nGates,
		     bad_flag, clip_gate, bnd, bad_flag_mask);

    for (int i=0; i<NGATES_4; i++) {
      //printf("i=%d\n", i);
      EXPECT_EQ(newData[i], newDataExpected[i]);
    }
  }

  //
  // flagged_add / multiply
  //

  TEST(FlagOps, flagged_add) {
    float data[NGATES_4] = {3,4,5,-6};
    bool bnd[NGATES_4] = {true, true, true, true};
    float bad_flag = -3;

    size_t nGates = NGATES_4;
    size_t clip_gate = nGates;
    bool bad_flag_mask[NGATES_4] = {false, true, true, true};
    bool multiply = true;
    float some_const = 10.0;

    float newData[NGATES_4] =         {0,0,0,0};
    float newDataExpected[NGATES_4] = {3,40,50,-60};

    se_flagged_add(some_const, multiply, data, newData, nGates,
                     bad_flag, clip_gate, bnd, bad_flag_mask);

    for (int i=0; i<NGATES_4; i++)
      EXPECT_EQ(newData[i], newDataExpected[i]);
  }

  TEST(FlagOps, flagged_add_clip_gate_out_of_bounds) {
    float data[NGATES_4] = {3,4,5,-6};
    bool bnd[NGATES_4] = {true, true, true, true};
    float bad_flag = -3;

    size_t nGates = NGATES_4;
    size_t clip_gate = nGates*2;
    bool bad_flag_mask[NGATES_4] = {false, true, false, false};
    bool multiply = false;
    float some_const = 2.0;

    float newData[NGATES_4] =         {0,0,0,0};
    float newDataExpected[NGATES_4] = {3,6,5,-6};

    se_flagged_add(some_const, multiply, data, newData, nGates,
                     bad_flag, clip_gate, bnd, bad_flag_mask);

    for (int i=0; i<NGATES_4; i++)
      EXPECT_EQ(newData[i], newDataExpected[i]);
  }

  TEST(FlagOps, flagged_add_with_clip_gate) {
    float data[NGATES_4] = {3,4,5,-6};
    bool bnd[NGATES_4] = {true, true, true, true};
    float bad_flag = -3;

    size_t nGates = NGATES_4;
    size_t clip_gate = nGates-2;
    bool bad_flag_mask[NGATES_4] = {false, true, false, false};
    bool multiply = false;
    float some_const = 2.0;

    float newData[NGATES_4] =         {0,0,0,0};
    float newDataExpected[NGATES_4] = {3,6,5,-6};

    se_flagged_add(some_const, multiply, data, newData, nGates,
		     bad_flag, clip_gate, bnd, bad_flag_mask);

    for (int i=0; i<NGATES_4; i++)
      EXPECT_EQ(newData[i], newDataExpected[i]);
  }

  TEST(FlagOps, flagged_add_with_bad_data) {
    float data[NGATES_4] = {-3,4,5,-6};
    bool bnd[NGATES_4] = {true, true, true, true};
    float bad_flag = -3;

    size_t nGates = NGATES_4;
    size_t clip_gate = nGates;
    bool bad_flag_mask[NGATES_4] = {true, true, false, true};
    bool multiply = false;
    float some_const = 2.0;

    float newData[NGATES_4] =         { 0,0,0,0};
    float newDataExpected[NGATES_4] = {-3,6,5,-4};

    se_flagged_add(some_const, multiply, data, newData, nGates,
                     bad_flag, clip_gate, bnd, bad_flag_mask);

    for (int i=0; i<NGATES_4; i++)
      EXPECT_EQ(newData[i], newDataExpected[i]);
  }

  TEST(FlagOps, flagged_add_with_boundary) {
    float data[NGATES_4] = {3,4,5,-6};
    bool bnd[NGATES_4] = {true, false, true, false};
    float bad_flag = -3;

    size_t nGates = NGATES_4;
    size_t clip_gate = nGates;
    bool bad_flag_mask[NGATES_4] = {true, true, true, true};
    bool multiply = false;
    float some_const = 2.0;

    float newData[NGATES_4] =         {0,0,0,0};
    float newDataExpected[NGATES_4] = {5,4,7,-6};

    se_flagged_add(some_const, multiply, data, newData, nGates,
                     bad_flag, clip_gate, bnd, bad_flag_mask);

    for (int i=0; i<NGATES_4; i++)
      EXPECT_EQ(newData[i], newDataExpected[i]);
  }


  //
  // clear_bad_flags
  //

  TEST(FlagOps, clear_bad_flags_complement) {

    size_t nGates = NGATES_4;
    bool bad_flag_mask[NGATES_4] = {true, false, false, true};
    bool bad_flag_mask_expected[NGATES_4] = {false, true, true, false};
    bool complement = true;

    se_clear_bad_flags(complement, nGates, bad_flag_mask);

    for (int i=0; i<NGATES_4; i++)
      EXPECT_EQ(bad_flag_mask[i], bad_flag_mask_expected[i]);
  }

  TEST(FlagOps, clear_bad_flags) {

    size_t nGates = NGATES_4;
    bool bad_flag_mask[NGATES_4] = {true, false, false, true};
    bool bad_flag_mask_expected[NGATES_4] = {false, false, false, false};
    bool complement = false;

    se_clear_bad_flags(complement, nGates, bad_flag_mask);

    for (int i=0; i<NGATES_4; i++)
      EXPECT_EQ(bad_flag_mask[i], bad_flag_mask_expected[i]);
  }

  //
  // copy_bad_flags
  //

  TEST(FlagOps, copy_bad_flags) {
    float data[NGATES_4] = {-3,4,-3,-6};
    bool bnd[NGATES_4] = {true, true, true, true};
    float bad_flag = -3;

    size_t nGates = NGATES_4;
    size_t clip_gate = nGates;
    bool bad_flag_mask[NGATES_4] = {true, false, false, true};
    bool bad_flag_mask_expected[NGATES_4] = {true, false, true, false};

    se_copy_bad_flags(data, nGates, bad_flag, clip_gate,
                      bnd, bad_flag_mask);

    for (int i=0; i<NGATES_4; i++)
      EXPECT_EQ(bad_flag_mask[i], bad_flag_mask_expected[i]);
  }

  TEST(FlagOps, copy_bad_flags_clip_gate) {
    float data[NGATES_4] = {-3,4,-3,-6};
    bool bnd[NGATES_4] = {true, true, true, true};
    float bad_flag = -3;

    size_t nGates = NGATES_4;
    size_t clip_gate = nGates-2;
    bool bad_flag_mask[NGATES_4] = {true, false, false, true};
    bool bad_flag_mask_expected[NGATES_4] = {true, false, true, true};

    se_copy_bad_flags(data, nGates, bad_flag, clip_gate,
                      bnd, bad_flag_mask);

    for (int i=0; i<NGATES_4; i++)
      EXPECT_EQ(bad_flag_mask[i], bad_flag_mask_expected[i]);
  }

  TEST(FlagOps, copy_bad_flags_boundary) {
    float data[NGATES_4] = {-3,-3,-3,-3};
    bool bnd[NGATES_4] = {true, false, true, false};
    float bad_flag = -3;

    size_t nGates = NGATES_4;
    size_t clip_gate = nGates;
    bool bad_flag_mask[NGATES_4] = {true, false, false, true};
    bool bad_flag_mask_expected[NGATES_4] = {true, false, true, true};

    se_copy_bad_flags(data, nGates, bad_flag, clip_gate, 
                      bnd, bad_flag_mask);

    for (int i=0; i<NGATES_4; i++) {
      //printf("i=%d\n", i);
      EXPECT_EQ(bad_flag_mask[i], bad_flag_mask_expected[i]);
    }
  }

  // These don't work??? They are supposed to mark gates with above average changes
  // but the code marks the gates strangely.
 
#define NGATES_8 8
 
  TEST(FlagOps, flag_glitches_happy_day) {
    //                      F F T  F  T T T T  
    float data[NGATES_8] = {3,4,5,-6,-7,4,4,5};
    //float newData[NGATES_8] = {0,0,0,0};
    bool bnd[NGATES_8] = {true, true, true, true, true, true, true, true};
    float bad_flag = -3;

    size_t nGates = NGATES_8;
    size_t clip_gate = nGates;
    bool bad_flag_mask_expected[NGATES_8] = {false, false, true, false, true, true, true, true};
    float deglitch_threshold = 3;
    int deglitch_radius = 1;
    int deglitch_min_bins = 3;
    bool bad_flag_mask[NGATES_8] = {false, false, false, false, true, true, true, true};
 
    se_flag_glitches(deglitch_threshold, deglitch_radius,
                         deglitch_min_bins,
                         data, nGates, 
			 bad_flag, clip_gate, bnd,
                         bad_flag_mask);
    for (int i=0; i<NGATES_8; i++) {
      std::cout << "i=" << i << std::endl;
      EXPECT_EQ(bad_flag_mask[i], bad_flag_mask_expected[i]);
    }
    
  }
}

