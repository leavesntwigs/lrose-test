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


  // These don't work???
  
  TEST(FlagOps, flag_glitches_happy_day) {

    float data[NGATES_4] = {3,4,5,-6};
    //float newData[NGATES_4] = {0,0,0,0};
    bool bnd[NGATES_4] = {true, true, true, true};
    float bad_flag = -3;

    size_t nGates = NGATES_4;
    size_t clip_gate = nGates;
    bool bad_flag_mask_expected[NGATES_4] = {false, false, false, true};
    float deglitch_threshold = 3;
    int deglitch_radius = 1;
    int deglitch_min_bins = 3;
    bool bad_flag_mask[NGATES_4] = {false, false, false, false};
 
    se_flag_glitches(deglitch_threshold, deglitch_radius,
                         deglitch_min_bins,
                         data, nGates, 
			 bad_flag, clip_gate, bnd,
                         bad_flag_mask);
    for (int i=0; i<NGATES_4; i++) {
      std::cout << "i=" << i << std::endl;
      EXPECT_EQ(bad_flag_mask[i], bad_flag_mask_expected[i]);
    }
    
  }
/*   
  TEST(SoloGenericUnfolding, fold__no_clipping__no_bad_flags__no_boundary) {

    float data[NGATES_4] = {1,1,1,1};
    float newData[NGATES_4] = {0,0,0,0};
    bool bnd[NGATES_4] = {1,1,1,1};
    float bad_flag = -3;

    // Nyquist stuff ...
    // the Nyquist velocity is less than some data values, 
    // should see unfolding
    float nyquist_velocity = 3.2; 

    // fold some data
    int nyquist_interval = 2 * nyquist_velocity;
    data[1] = data[1] + 2 * (int) nyquist_interval;
    data[3] = data[3] - 1 * (int) nyquist_interval;

    size_t nGates = NGATES_4;
    size_t clip_gate = nGates;
    float newData_expected[NGATES_4] = {1,1,1,1};

    size_t ngates_averaged = 3;
    float v0 = 1.0;
    int max_pos_folds = 5;
    int max_neg_folds = 5;

    se_BB_generic_unfold(data, newData, nGates, 
			 &v0, ngates_averaged,
			 nyquist_velocity,
			 max_pos_folds, max_neg_folds,
			 bad_flag, clip_gate, bnd);
    for (int i=0; i<NGATES_4; i++)
      EXPECT_EQ(newData[i], newData_expected[i]);
    // verify last good initial velocity
    EXPECT_EQ(v0, 1.0); 
  }
  
  TEST(SoloGenericUnfolding, fold__clip_gate__bad_flags__no_boundary) {

    float data[NGATES_4] =    {-3,1,1,1};
    float newData[NGATES_4] = { 0,0,0,0};
    bool bnd[NGATES_4] = {1,1,1,1};
    float bad_flag = -3;

    // Nyquist stuff ...
    // the Nyquist velocity is less than some data values, 
    // should see unfolding
    float nyquist_velocity = 3.2; 

    // fold some data
    int nyquist_interval = 2 * nyquist_velocity;
    data[1] = data[1] + 2 * (int) nyquist_interval;
    data[3] = data[3] - 1 * (int) nyquist_interval;

    size_t nGates = NGATES_4;
    size_t clip_gate = 3;
    float newData_expected[NGATES_4] = {-3,1,1,-5};

    size_t ngates_averaged = 3;
    float v0 = 1.0;
    int max_pos_folds = 5;
    int max_neg_folds = 5;

    se_BB_generic_unfold(data, newData, nGates, 
			 &v0, ngates_averaged,
			 nyquist_velocity,
			 max_pos_folds, max_neg_folds,
			 bad_flag, clip_gate, bnd);
    for (int i=0; i<NGATES_4; i++)
      EXPECT_EQ(newData[i], newData_expected[i]);
    // verify last good initial  velocity
    float expected_v0 = 1.0;
    EXPECT_EQ(v0, expected_v0);

  }
  
  TEST(SoloGenericUnfolding, fold_exceeds_max_folds__no_clip_gate__bad_flags__no_boundary) {

    float data[NGATES_4] = {-3,10,-3,10};
    float newData[NGATES_4] = {0,0,0,0};
    bool bnd[NGATES_4] = {1,1,1,1};
    float bad_flag = -3;

    size_t ngates_averaged = 3;
    float v0 = 10.0;
    // think about which way we need to unfold, in the negative direction, or in the positive direction
    int max_pos_folds = 3;  // used when velocity < running average; need to move in positive direction
    int max_neg_folds = 2;  // used when velocity > running average; need to move the velocity in the negative direction

    float nyquist_velocity = 5.0; // causes folding
    // fold some data
    int nyquist_interval = 2 * nyquist_velocity;

    float newData_expected[NGATES_4] = {-3,1,-3,1};
    // these will be limited by the max number of unfolds
    newData_expected[1] = data[1] - (2) * (int) nyquist_interval; // 10 - 20 = -10
    newData_expected[3] = data[3] + (1) * (int) nyquist_interval; // 10 + 10 =  20

    data[1] = data[1] - (max_pos_folds+2) * (int) nyquist_interval; // 10 - 50 = -40
    data[3] = data[3] + (max_neg_folds+1) * (int) nyquist_interval; // 10 + 30 =  40

    size_t nGates = NGATES_4;
    size_t clip_gate = nGates;

    se_BB_generic_unfold(data, newData, nGates, 
			 &v0, ngates_averaged,
			 nyquist_velocity,
			 max_pos_folds, max_neg_folds,
			 bad_flag, clip_gate, bnd);
    for (int i=0; i<NGATES_4; i++)
      EXPECT_EQ(newData[i], newData_expected[i]);
    // verify last good initial velocity
    float expected_v0 = -10.0; //(10.0 + (10-2*nyquist_interval) + (10+1*nyquist_interval))/3.0;
    EXPECT_FLOAT_EQ(v0, expected_v0);

  }

  TEST(SoloGenericUnfolding, fold_at_max_folds__no_clip_gate__bad_flags__no_boundary) {

    float data[NGATES_4] = {-3,7,7,-3};
    float newData[NGATES_4] = {0,0,0,0};
    bool bnd[NGATES_4] = {1,1,1,1};
    float bad_flag = -3;

    size_t ngates_averaged = 3;
    float v0 = 7.0;
    int max_pos_folds = 3;
    int max_neg_folds = 2;

    float nyquist_velocity = 5.0; // causes folding
    // fold some data
    int nyquist_interval = 2 * nyquist_velocity;


    size_t nGates = NGATES_4;
    size_t clip_gate = nGates;
    float newData_expected[NGATES_4] = {-3,7,7,-3};
    // these will be limited by the max number of unfolds
    //    newData_expected[1] = data[1] + (max_pos_folds) * (int) nyquist_interval;
    //newData_expected[2] = data[2] - (max_neg_folds) * (int) nyquist_interval;
    float expected_v0 = v0; // (10.0 + (10+2*nyquist_interval) + (10-1*nyquist_interval))/3.0;

    data[1] = v0 - (max_pos_folds) * (int) nyquist_interval;
    data[2] = v0 + (max_neg_folds) * (int) nyquist_interval;

    se_BB_generic_unfold(data, newData, nGates, 
			 &v0, ngates_averaged,
			 nyquist_velocity,
			 max_pos_folds, max_neg_folds,
			 bad_flag, clip_gate, bnd);
    for (int i=0; i<NGATES_4; i++)
      EXPECT_EQ(newData[i], newData_expected[i]);
    // verify last good initial velocity
    EXPECT_EQ(v0, expected_v0);

  }

  // Tests for calculating v0 ...
  TEST(SoloUnfolding, calculate_v0_using_ac_wind) {

    float data[NGATES_4] = {3,4,5,6};
    float newData[NGATES_4] = {0,0,0,0};
    bool bnd[NGATES_4] = {1,1,1,1};
    float bad_flag = -3;
    size_t ngates_averaged = 3;
    int max_pos_folds = 5;
    int max_neg_folds = 5;

    float nyquist_velocity = 10.0;
    float dds_radd_eff_unamb_vel = 0.0;
    float azimuth_angle_degrees = 360.0;
    float elevation_angle_degrees = 90.0;
    float ew_horiz_wind = 999;
    float ns_horiz_wind = 999;
    float vert_wind = 2.0;
    //    float v0_expected = vert_wind; // since cos(90) = 0 only w*sin(elev) term is non-zero for v0 calculation

    size_t nGates = NGATES_4;
    size_t clip_gate = nGates;
    float newData_expected[NGATES_4] = {3, 4, 5, 6};


    se_BB_unfold_ac_wind(data, newData, nGates,
			 nyquist_velocity, dds_radd_eff_unamb_vel,
			 azimuth_angle_degrees, elevation_angle_degrees,
			 ew_horiz_wind,
			 ns_horiz_wind,
			 vert_wind,
			 max_pos_folds, max_neg_folds,
			 ngates_averaged,
			 bad_flag, clip_gate, bnd);

    for (int i=0; i<NGATES_4; i++)
      EXPECT_EQ(newData[i], newData_expected[i]);

  }

  TEST(SoloUnfolding, calculate_v0_using_local_wind) {

    float data[NGATES_4] = {3,4,5,6};
    float newData[NGATES_4] = {0,0,0,0};
    bool bnd[NGATES_4] = {1,1,1,1};
    float bad_flag = -3;
    size_t ngates_averaged = 3;
    int max_pos_folds = 5;
    int max_neg_folds = 5;

    float nyquist_velocity = 10.0;
    float dds_radd_eff_unamb_vel = 0.0;
    float azimuth_angle_degrees = 360.0;
    float elevation_angle_degrees = 90.0;
    float ew_horiz_wind = 999;
    float ns_horiz_wind = 999;
    float vert_wind = 2.0;
    //float v0_expected = vert_wind; // since cos(90) = 0 only w*sin(elev) term is non-zero for v0 calculation

    size_t nGates = NGATES_4;
    size_t clip_gate = nGates;
    float newData_expected[NGATES_4] = {3, 4, 5, 6};


    se_BB_unfold_local_wind(data, newData, nGates,
			 nyquist_velocity, dds_radd_eff_unamb_vel,
			 azimuth_angle_degrees, elevation_angle_degrees,
			 ew_horiz_wind,
			 ns_horiz_wind,
			 vert_wind,
			 max_pos_folds, max_neg_folds,
			 ngates_averaged,
			 bad_flag, clip_gate, bnd);

    for (int i=0; i<NGATES_4; i++)
      EXPECT_EQ(newData[i], newData_expected[i]);

  }

  TEST(SoloUnfolding, calculate_v0_using_first_good_gate) {

    float data[NGATES_4] = {3,4,5,6};
    float newData[NGATES_4] = {0,0,0,0};
    bool bnd[NGATES_4] = {1,1,1,1};
    float bad_flag = -3;
    size_t ngates_averaged = 3;
    int max_pos_folds = 5;
    int max_neg_folds = 5;

    float nyquist_velocity = 10.0;
    float dds_radd_eff_unamb_vel = 0.0;
    //float azimuth_angle_degrees = 360.0;
    //float elevation_angle_degrees = 90.0;
    float last_good_v0 = bad_flag;
    float v0_expected = data[0];

    size_t nGates = NGATES_4;
    size_t clip_gate = nGates;
    float newData_expected[NGATES_4] = {3, 4, 5, 6};


    se_BB_unfold_first_good_gate(data, newData, nGates,
			 nyquist_velocity, dds_radd_eff_unamb_vel,
				 // azimuth_angle_degrees, elevation_angle_degrees,
			 max_pos_folds, max_neg_folds,
			 ngates_averaged,
			 &last_good_v0,
			 bad_flag, clip_gate, bnd);

    for (int i=0; i<NGATES_4; i++)
      EXPECT_EQ(newData[i], newData_expected[i]);

    // verify initial velocity
    EXPECT_EQ(last_good_v0, v0_expected);

  }

  TEST(SoloUnfolding, calculate_v0_using_first_good_gate__bad_data) {

    float data[NGATES_4] = {-3,-3,5,6};
    float newData[NGATES_4] = {0,0,0,0};
    bool bnd[NGATES_4] = {1,1,1,1};
    float bad_flag = -3;
    size_t ngates_averaged = 3;
    int max_pos_folds = 5;
    int max_neg_folds = 5;

    float nyquist_velocity = 10.0;
    float dds_radd_eff_unamb_vel = 0.0;
    //float azimuth_angle_degrees = 360.0;
    //float elevation_angle_degrees = 90.0;
    float last_good_v0 = bad_flag;
    float v0_expected = data[2];

    size_t nGates = NGATES_4;
    size_t clip_gate = nGates;
    float newData_expected[NGATES_4] = {-3, -3, 5, 6};


    se_BB_unfold_first_good_gate(data, newData, nGates,
			 nyquist_velocity, dds_radd_eff_unamb_vel,
				 //		 azimuth_angle_degrees, elevation_angle_degrees,
			 max_pos_folds, max_neg_folds,
			 ngates_averaged,
			 &last_good_v0,
			 bad_flag, clip_gate, bnd);

    for (int i=0; i<NGATES_4; i++)
      EXPECT_EQ(newData[i], newData_expected[i]);

    // verify initial velocity
    EXPECT_EQ(last_good_v0, v0_expected);

  }

  TEST(SoloUnfolding, calculate_v0_using_first_good_gate_2nd_trip) {

    float data[NGATES_4] = {3,4,5,6};
    float newData[NGATES_4] = {0,0,0,0};
    bool bnd[NGATES_4] = {1,1,1,1};
    float bad_flag = -3;
    size_t ngates_averaged = 3;
    int max_pos_folds = 5;
    int max_neg_folds = 5;

    float nyquist_velocity = 10.0;
    float dds_radd_eff_unamb_vel = 0.0;
    //float azimuth_angle_degrees = 360.0;
    //float elevation_angle_degrees = 90.0;
    float last_good_v0 = 9;
    float v0_expected = data[0];

    size_t nGates = NGATES_4;
    size_t clip_gate = nGates;
    float newData_expected[NGATES_4] = {3, 4, 5, 6};


    se_BB_unfold_first_good_gate(data, newData, nGates,
			 nyquist_velocity, dds_radd_eff_unamb_vel,
				 //		 azimuth_angle_degrees, elevation_angle_degrees,
			 max_pos_folds, max_neg_folds,
			 ngates_averaged,
			 &last_good_v0,
			 bad_flag, clip_gate, bnd);

    for (int i=0; i<NGATES_4; i++)
      EXPECT_EQ(newData[i], newData_expected[i]);

    // verify initial velocity
    EXPECT_EQ(last_good_v0, v0_expected);

  }

*/  

  // Boundary tests ... 

 
  /*  

  TEST(SoloUnfolding, ac_vel_folded__with_max_vel_instead_of_nyquist__clip_gate__no_boundary) {

    float data[NGATES_4] = {-4,-3, 5, 8};
    float newData[NGATES_4] = {0,0,0,0};
    bool bnd[NGATES_4] = {1,1,1,1};
    float bad_flag = -3;

    float vert_velocity = 3;
    float ew_velocity = 10.0;
    float ns_velocity = 0.0;
    float ew_gndspd_corr = 1;  // ac_vel should be 11.0
    float tilt = M_PI/2.0; // or any multiple of pi help make ac_vel = 0
    float elevation = 0.0; // or any multiple of pi help make ac_vel = 0
    // ac_vel should be unfolded to -1.0

    // Nyquist stuff ...
    // keep the Nyquist velocity greater than any data value, 
    // to avoid any folding/unfolding
    float eff_unamb_vel = 6.0;  // causes folding
    float nyquist_velocity = 0.0; 

    size_t nGates = NGATES_4;
    size_t clip_gate = 3;
    float newData_expected[NGATES_4] = {-5,-3,4,8};  // no change 

    se_remove_ac_motion(vert_velocity, ew_velocity, ns_velocity,
                        ew_gndspd_corr, tilt, elevation,
                        data, newData, nGates, bad_flag, clip_gate,
                        eff_unamb_vel, nyquist_velocity, bnd);

    for (int i=0; i<NGATES_4; i++)
      EXPECT_EQ(newData[i], newData_expected[i]);
  }

  // Boundary tests ...

  // *  TEST(SoloUnfolding, no_fold__unfold__no_clipping__no_bad_flags__boundary) 
  // *   TEST(SoloUnfolding, fold__no_folding__clip_gate__bad_flags__boundary) 
  // *     TEST(SoloUnfolding, fold__folding_clip_gate__bad_flags__boundary) 
  // *	TEST(SoloUnfolding, ac_vel_folded__clip_gate__boundary) 
  //   *  TEST(SoloUnfolding, ac_vel_folded__with_max_vel_instead_of_nyquist__clip_gate__boundary)

  // *  TEST( ... remove_multifolded_ac_vel_remove_single_folded_velocity NOTE:  shortcoming of remove aircraft vel
  
  */
/*
  TEST(SoloUnfolding, folding__fgg__no_clipping__no_bad_flags__boundary) {

#define NGATES_7 7

    float data[NGATES_7] =    {3,-3, 5,-16, 7,-3 ,6};
    float newData[NGATES_7] = {0, 0, 0,  0, 0, 0, 0};
    bool bnd[NGATES_7] =      {0, 0, 1,  1, 0, 1, 1};
    float bad_flag = -3;

    // Nyquist stuff ...                                                                                              
    // the Nyquist velocity is less than some data values,                                                            
    // should see unfolding                                                                                           
    float eff_unamb_vel = 0.0; // TODO: this comes from data file?                                                    
    float nyquist_velocity = 3.2;
    float last_good_v0 = bad_flag;
    int max_pos_folds = 5;
    int max_neg_folds = 5;

    size_t nGates = NGATES_7;
    size_t clip_gate = nGates;
    size_t ngates_averaged = 2;

    //                              v4:      3   4       3.5
    //                         v4 - vx:     -2  20      -2.5
    float newData_expected[NGATES_7] = {3,-3,5,  2, 7,-3, 6};
  //float newData_expected[NGATES_7] = {3,-3,-1,-10, 7,-3, 0};  // this is the same unfolding using remove_ac_motion
    float v0_expected = 5;

    se_BB_unfold_first_good_gate(data, newData, nGates,
			 nyquist_velocity, eff_unamb_vel,
			 max_pos_folds, max_neg_folds,
			 ngates_averaged,
			 &last_good_v0,
			 bad_flag, clip_gate, bnd);

    // verify initial velocity
    EXPECT_EQ(last_good_v0, v0_expected);

    for (int i=0; i<NGATES_7; i++)
      EXPECT_EQ(newData[i], newData_expected[i]);


  }

  

  TEST(SoloUnfolding, no_folding__local_wind__ngates_averaged_1__clip_gate__bad_flags__boundary) {
#define NGATES_10 10

    float data[NGATES_10] =                { 3,-3, -3, 5, 5,-2, -3, 5, 5, -3};
    float newData[NGATES_10] =             { 0, 0,  0, 0, 0, 0,  0, 0, 0,  0};
    //                                  v4:  3         3     5     -2
    //                             v4 - vx:  0        -5     7     -7
    float newData_expected[NGATES_10] =    { 3,-3, -3, 5, 5,-2, -3, 5, 5, -3}; 
 // float newData_expected[NGATES_10] =    { 6,-3, -3, 8, 5, 1, -3, 8, 5, -3}; // results using remove_ac_motion
    bool  bnd[NGATES_10] =                 { 1, 0,  1, 1, 0, 1,  1, 1, 1,  0};
    float bad_flag = -3;

    // Nyquist stuff ...     
    // keep the Nyquist velocity greater than any data value,
    // to avoid any folding/unfolding 
    float eff_unamb_vel = 0.0;
    float nyquist_velocity = 10.0;

    size_t nGates = NGATES_10;
    size_t clip_gate = 8;

    float azimuth_angle_degrees = 360.0;
    float elevation_angle_degrees = 90.0;
    float ew_horiz_wind = 999;
    float ns_horiz_wind = 999;
    float vert_wind = 3.0;
    //float v0_expected = vert_wind; // since cos(90) = 0 only w*sin(elev) term is non-zero for v0 calculation

    size_t ngates_averaged = 1;
    int max_pos_folds = 5;
    int max_neg_folds = 5;

    se_BB_unfold_local_wind(data, newData, nGates,
			 nyquist_velocity, eff_unamb_vel,
			 azimuth_angle_degrees, elevation_angle_degrees,
			 ew_horiz_wind,
			 ns_horiz_wind,
			 vert_wind,
			 max_pos_folds, max_neg_folds,
			 ngates_averaged,
			 bad_flag, clip_gate, bnd);


    for (int i=0; i<NGATES_10; i++)
      EXPECT_EQ(newData[i], newData_expected[i]);
  }
  
  TEST(SoloUnfolding, folding__local_wind__ngates_averaged_1__no_clip_gate__bad_flags__boundary) {

    float data[NGATES_10] =             { 6,-3,  4,-5, 9, 5, -3, 8, 8, -3};
    float newData[NGATES_10] =          { 0, 0,  0, 0, 0, 0,  0, 0, 0,  0};
    //                                v4: 6         6  7         9  8
    // then unfold by nyqi = 6            0  x      7, 9,        8, 8,  x
    float newData_expected[NGATES_10] = { 6,-3,  4, 7, 9, 5, -3, 8, 8, -3};
    bool  bnd[NGATES_10] =              { 1, 1,  0, 1, 1, 0,  0, 1, 1,  1};
    float bad_flag = -3;

    // Nyquist stuff ...    
    // keep the Nyquist velocity greater than any data value,
    // to avoid any folding/unfolding 
    float eff_unamb_vel = 0.0;
    float nyquist_velocity = 3.0;

    int nGates = NGATES_10;
    int clip_gate = nGates;

    float azimuth_angle_degrees = 270.0;
    float elevation_angle_degrees = 0.0;
    float ew_horiz_wind = -6;
    float ns_horiz_wind = 999;
    float vert_wind = 33.0;
    //float v0_expected = ew_horiz_wind; // since sin(0) = 0 only u*sin(az)=ew_horiz_wind*(-1) term is non-zero for v0 calculation

    size_t ngates_averaged = 1;
    int max_pos_folds = 5;
    int max_neg_folds = 5;

    se_BB_unfold_local_wind(data, newData, nGates,
			 nyquist_velocity, eff_unamb_vel,
			 azimuth_angle_degrees, elevation_angle_degrees,
			 ew_horiz_wind,
			 ns_horiz_wind,
			 vert_wind,
			 max_pos_folds, max_neg_folds,
			 ngates_averaged,
			 bad_flag, clip_gate, bnd);

    for (int i=0; i<NGATES_10; i++)
      EXPECT_EQ(newData[i], newData_expected[i]);
  }
*/
  /*
  TEST(SoloUnfolding, folding__ngates_average_1__clip_gate__boundary) {

    float data[NGATES_10] =             {-3,-3, -3, 5,-5, 5, -3, 5, 5, -3};
    float newData[NGATES_10] =          { 0, 0,  0, 0, 0, 0,  0, 0, 0,  0};
    //   add fold                              x,12, 2
    //   unfold                                  x,-8, 2
    float newData_expected[NGATES_10] = {-3,-3, -3,-8, 2, 5, -3, 5, 5, -3};
    bool  bnd[NGATES_10] =              { 0, 0,  1, 1, 1, 0,  0, 0, 0,  0};

    float bad_flag = -3;

    float vert_velocity = 33.67; // goes with sin(elevation)
    float ew_velocity = 1;   // these three go with sin(tilt)
    float ns_velocity = 1;
    float ew_gndspd_corr = 1;
    float elevation = - M_PI/2.0; // or any multiple of pi help make ac_vel = 0 
    float tilt = 0.0; // or any multiple of pi help make ac_vel = 0  
    // fold should be 7.0 

    // Nyquist stuff ...    
    // keep the Nyquist velocity greater than any data value,
    // to avoid any folding/unfolding 
    float eff_unamb_vel = 0.0;
    float nyquist_velocity = 10.0;

    size_t nGates = NGATES_10;
    size_t clip_gate = 8;

    float azimuth_angle_degrees = 360.0;
    float elevation_angle_degrees = 90.0;
    float ew_horiz_wind = 999;
    float ns_horiz_wind = 999;
    float vert_wind = 2.0;
    //float v0_expected = vert_wind; // since cos(90) = 0 only w*sin(elev) term is non-zero for v0 calculation

    size_t ngates_averaged = 3;
    int max_pos_folds = 5;
    int max_neg_folds = 5;

    se_BB_unfold_local_wind(data, newData, nGates,
			 nyquist_velocity, eff_unamb_vel,
			 azimuth_angle_degrees, elevation_angle_degrees,
			 ew_horiz_wind,
			 ns_horiz_wind,
			 vert_wind,
			 max_pos_folds, max_neg_folds,
			 ngates_averaged,
			 bad_flag, clip_gate, bnd);


    for (int i=0; i<NGATES_10; i++)
      EXPECT_EQ(newData[i], newData_expected[i]);
   }


  
  TEST(SoloUnfolding, folding__ngates_average_3) {
 
    float data[NGATES_10] =             {-3,-3, -3, 5, 6,-4, -3,10,-12, -3};
    float newData[NGATES_10] =          { 0, 0,  0, 0, 0, 0,  0, 0, 0,   0};
    //    fold by -1                              4  5 -5   x  9 -13
    //   unfold                                     0  1 -1   x  5  -9
    float newData_expected[NGATES_10] = {-3,-3, -3, 0, 1,-1, -3, 5, -9, -3};
    bool  bnd[NGATES_10] =              { 1, 1,  1, 1, 1, 1,  1, 1,  1,  1};

    float bad_flag = -3;

    // Nyquist stuff ...    
    // keep the Nyquist velocity greater than any data value,
    // to avoid any folding/unfolding 
    float eff_unamb_vel = 0.0;
    float nyquist_velocity = 2.0;

    size_t nGates = NGATES_10;
    size_t clip_gate = nGates;

    int max_pos_folds = 5;
    int max_neg_folds = 5;

    se_BB_unfold_first_good_gate(data, newData, nGates,
			 nyquist_velocity, dds_radd_eff_unamb_vel,
				 // azimuth_angle_degrees, elevation_angle_degrees,
			 max_pos_folds, max_neg_folds,
			 ngates_averaged,
			 &last_good_v0,
			 bad_flag, clip_gate, bnd);

    // verify initial velocity
    EXPECT_EQ(last_good_v0, v0_expected);

    for (int i=0; i<NGATES_10; i++)
      EXPECT_EQ(newData[i], newData_expected[i]);

  }
  */
  
  /*
  TEST(SoloUnfolding, folding__with_max_vel_instead_of_nyquist__clip_gate__boundary) {
 
    float data[NGATES_10] =             {-3,-3, -3, 5,-5, 5, -3, 5, 5,  5};
    float newData[NGATES_10] =          { 0, 0,  0, 0, 0, 0,  0, 0, 0,  0};
    //   add fold                              x,12, 2           12
    //   unfold                                  x,-8, 2           -8
    float newData_expected[NGATES_10] = {-3,-3, -3,-8, 2, 5, -3, 5,-8,  5};
    bool  bnd[NGATES_10] =              { 0, 0,  1, 1, 1, 0,  0, 0, 1,  1};

    float bad_flag = -3;

    float vert_velocity = 33.67; // goes with sin(elevation)
    float ew_velocity = 1;   // these three go with sin(tilt)
    float ns_velocity = 1;
    float ew_gndspd_corr = 1;
    float elevation = - M_PI/2.0; // or any multiple of pi help make ac_vel = 0 
    float tilt = 0.0; // or any multiple of pi help make ac_vel = 0  
    // fold should be 7.0 

    // Nyquist stuff ...    
    // keep the Nyquist velocity greater than any data value,
    // to avoid any folding/unfolding 
    float eff_unamb_vel = 10.0;
    float nyquist_velocity = 0.0;

    size_t nGates = NGATES_10;
    size_t clip_gate = 9;

    float azimuth_angle_degrees = 360.0;
    float elevation_angle_degrees = 90.0;
    float ew_horiz_wind = 999;
    float ns_horiz_wind = 999;
    float vert_wind = 2.0;
    //float v0_expected = vert_wind; // since cos(90) = 0 only w*sin(elev) term is non-zero for v0 calculation

    int max_pos_folds = 5;
    int max_neg_folds = 5;

    se_BB_unfold_local_wind(data, newData, nGates,
			 nyquist_velocity, dds_radd_eff_unamb_vel,
			 azimuth_angle_degrees, elevation_angle_degrees,
			 ew_horiz_wind,
			 ns_horiz_wind,
			 vert_wind,
			 max_pos_folds, max_neg_folds,
			 ngates_averaged,
			 bad_flag, clip_gate, bnd);



    for (int i=0; i<NGATES_10; i++)
      EXPECT_EQ(newData[i], newData_expected[i]);

  }
 
  
  TEST(SoloUnfolding, clipping__speckle_at_beginning__skip_speckle_at_end__no_boundary) {

    float data[NGATES_7] =             { 5, -3, -3, -3, 5, 5,-3};
    float newData[NGATES_7] =          { 0,  0,  0,  0, 0, 0, 0};
    float newData_expected[NGATES_7] = {-3, -3, -3, -3, 5, 5,-3};

    bool  bnd[NGATES_7] = {1,1,1,1,1,1,1};
    float bad_flag = -3;
    size_t nGates = NGATES_7;
    size_t clip_gate = 5;

    int max_pos_folds = 5;
    int max_neg_folds = 5;

    se_BB_unfold_first_good_gate(data, newData, nGates,
			 nyquist_velocity, dds_radd_eff_unamb_vel,
				 // azimuth_angle_degrees, elevation_angle_degrees,
			 max_pos_folds, max_neg_folds,
			 ngates_averaged,
			 &last_good_v0,
			 bad_flag, clip_gate, bnd);

    // verify initial velocity
    EXPECT_EQ(last_good_v0, v0_expected);

    for (int i=0; i<NGATES_7; i++)
      EXPECT_EQ(newData[i], newData_expected[i]);
  }

  TEST(SoloUnfolding, speckle_at_boundary_edges_ignored) {
    //                                   b,  g,  g,  b, b, g, g
    float data[NGATES_7] =             {-3,  5,  5, -3,-3, 5, 5};
    float newData[NGATES_7] =          { 0,  0,  0,  0, 0, 0, 0};
    float newData_expected[NGATES_7] = {-3,  5,  5, -3,-3, 5, 5}; // no change

    bool  bnd[NGATES_7] =              { 0,  0,  1,  1, 1, 1, 0};
    float bad_flag = -3;
    size_t nGates = NGATES_7;
    size_t clip_gate = 5;

    int max_pos_folds = 5;
    int max_neg_folds = 5;

    se_BB_unfold_first_good_gate(data, newData, nGates,
			 nyquist_velocity, dds_radd_eff_unamb_vel,
			 max_pos_folds, max_neg_folds,
			 ngates_averaged,
			 &last_good_v0,
			 bad_flag, clip_gate, bnd);

    // verify initial velocity
    EXPECT_EQ(last_good_v0, v0_expected);

    for (int i=0; i<NGATES_7; i++)
      EXPECT_EQ(newData[i], newData_expected[i]);
  }
  */

}  // namespace

