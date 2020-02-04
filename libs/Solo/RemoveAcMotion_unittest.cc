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
#define NGATES_4 4
  TEST(SoloRemoveAcMotion, no_adjust__no_clipping__no_bad_flags__no_boundary) {

    float data[NGATES_4] = {3,4,5,6};
    float newData[NGATES_4] = {0,0,0,0};
    bool bnd[NGATES_4] = {1,1,1,1};
    float bad_flag = -3;
    float vert_velocity = 1;
    float ew_velocity = 1;
    float ns_velocity = 1;
    float ew_gndspd_corr = 1;
    float elevation = 0.0; // or any multiple of pi help make ac_vel = 0
    float tilt = 0.0; // or any multiple of pi help make ac_vel = 0
    // ac_vel should be zero

    // Nyquist stuff ...
    // keep the Nyquist velocity greater than any data value
    float eff_unamb_vel = 0.0; // TODO: this comes from data file?
    float nyquist_velocity = 10.0; // TODO: ???

    size_t nGates = NGATES_4;
    size_t clip_gate = nGates;
    float newData_expected[NGATES_4] = {3, 4, 5, 6};

    se_remove_ac_motion(vert_velocity, ew_velocity, ns_velocity,
			ew_gndspd_corr, tilt, elevation,
			data, newData, nGates, bad_flag, clip_gate,
			eff_unamb_vel, nyquist_velocity, bnd);
    for (int i=0; i<NGATES_4; i++)
      EXPECT_EQ(newData[i], newData_expected[i]);
    
  }
  /*
  TEST(SoloRemoveAcMotion, speckle_outside_clip_gate__no_boundary) {

    // testing this pattern b|b|g|b  but clip gate should prevent the g (good) value
    // from being set to b (bad), i.e. considered a speckle and zapped.
    float data[NGATES_4] = {-3,-3,5,-3};
    float newData[NGATES_4] = {0,0,0,0};
    bool bnd[NGATES_4] = {1,1,1,1};
    float bad_flag = -3;
    int a_speckle = 1;

    size_t nGates = NGATES_4;
    size_t clip_gate = 2;
    float newData_expected[NGATES_4] = {-3,-3,5,-3};  // no changed 

    se_remove_ac_motion(data, newData, nGates, bad_flag, a_speckle, clip_gate, bnd);
    for (int i=0; i<NGATES_4; i++)
      EXPECT_EQ(newData[i], newData_expected[i]);
  }

  TEST(SoloRemoveAcMotion, speckle_inside_clip_gate__no_boundary) {

    // testing this pattern b|b|g|b  clip gate is just past good value
    // good value is NOT  considered a speckle and zapped.
    float data[NGATES_4] = {-3,-3,5,-3};
    float newData[NGATES_4] = {0,0,0,0};
    bool bnd[NGATES_4] = {1,1,1,1};
    float bad_flag = -3;
    int a_speckle = 1;

    size_t nGates = NGATES_4;
    size_t clip_gate = 3;
    float newData_expected[NGATES_4] = {-3,-3,5,-3};  // no change 

    se_remove_ac_motion(data, newData, nGates, bad_flag, a_speckle, clip_gate, bnd);
    for (int i=0; i<NGATES_4; i++)
      EXPECT_EQ(newData[i], newData_expected[i]);
  }


  // TODO:  Is this a speckle?  b|b|g|g|    when it is at the very end?  But we don't know the next value?
  // If end of data, then it is a speckle.
  // If it is the end of a clip gate, then it may or may NOT be a speckle, since we don't know the next value


  TEST(SoloRemoveAcMotion, no_clipping__speckle__no_boundary) {

#define NGATES_7 7

    float data[NGATES_7] =    {3,-3, 5, 5, 5,-3 ,6};
    float newData[NGATES_7] = {0, 0, 0, 0, 0, 0, 0};
    bool bnd[NGATES_7] =      {1, 1, 1, 1, 1, 1, 1};
    float bad_flag = -3;
    int a_speckle = 3;

    size_t nGates = NGATES_7;
    size_t clip_gate = nGates;
    float newData_expected[NGATES_7] = {-3,-3,-3,-3,-3,-3, -3};  // 3 speckles zapped 

    se_remove_ac_motion(data, newData, nGates, bad_flag, a_speckle, clip_gate, bnd);
    for (int i=0; i<NGATES_7; i++)
      EXPECT_EQ(newData[i], newData_expected[i]);
  }


  // should clear first speckle, but not second speckle because clip_gate ends 
  // before second speckle
  //   
  TEST(SoloRemoveAcMotion, clipping_ends_before_second_speckle__no_boundary) {
    // double bar (||) indicates clip_gate
    //                       g|b | b|  g| g| g|  b| g||g|  b|
#define NGATES_10 10

    float data[NGATES_10] =                { 3,-3, -3, 5, 5, 5, -3, 5, 5, -3};
    float newData[NGATES_10] =             { 0, 0,  0, 0, 0, 0,  0, 0, 0,  0};
    float newData_expected[NGATES_10] =    {-3,-3, -3,-3,-3,-3, -3, 5, 5, -3}; // 2 speckles zapped
    bool  bnd[NGATES_10] =                 { 1, 1,  1, 1, 1, 1,  1, 1, 1,  1};
    float bad_flag = -3;
    int a_speckle = 3;

    size_t nGates = NGATES_10;
    size_t clip_gate = 8;

    se_remove_ac_motion(data, newData, nGates, bad_flag, a_speckle, clip_gate, bnd);
    for (int i=0; i<NGATES_10; i++)
      EXPECT_EQ(newData[i], newData_expected[i]);
  }



  TEST(SoloRemoveAcMotion, clipping__speckle__boundary_ends_before_speckle) {
    //  no data changed
    float data[NGATES_10] =             { 3,-3, -3, 5, 5, 5, -3, 5, 5, -3};
    float newData[NGATES_10] =          { 0, 0,  0, 0, 0, 0,  0, 0, 0,  0};
    float newData_expected[NGATES_10] = {-3,-3, -3, 5, 5, 5, -3, 5, 5, -3};

    bool  bnd[NGATES_10] =              { 1, 1,  0, 0, 0, 0,  0, 0, 0,  0};
    float bad_flag = -3;
    int a_speckle = 3;

    int nGates = NGATES_10;
    int clip_gate = 8;

    se_remove_ac_motion(data, newData, nGates, bad_flag, a_speckle, clip_gate, bnd);
    for (int i=0; i<NGATES_10; i++)
      EXPECT_EQ(newData[i], newData_expected[i]);
  }

  TEST(SoloRemoveAcMotion, clipping__speckle__boundary_ends_in_middle_of_speckle) {

    //  no data changed
    float data[NGATES_10] =             {-3,-3, -3, 5, 5, 5, -3, 5, 5, -3};
    float newData[NGATES_10] =          { 0, 0,  0, 0, 0, 0,  0, 0, 0,  0};
    float newData_expected[NGATES_10] = {-3,-3, -3, 5, 5, 5, -3, 5, 5, -3};
    bool  bnd[NGATES_10] =              { 1, 1,  1, 1, 0, 0,  0, 0, 0,  0};

    float bad_flag = -3;
    size_t a_speckle = 3;
    size_t nGates = NGATES_10;
    size_t clip_gate = 8;

    se_remove_ac_motion(data, newData, nGates, bad_flag, a_speckle, clip_gate, bnd);
    for (int i=0; i<NGATES_10; i++)
      EXPECT_EQ(newData[i], newData_expected[i]);
   }

  TEST(SoloRemoveAcMotion, clipping__speckle__boundary_ends_beyond_speckle) {
 
    float data[NGATES_10] =             {-3,-3, -3, 5, 5, 5, -3, 5, 5, -3};
    float newData[NGATES_10] =          { 0, 0,  0, 0, 0, 0,  0, 0, 0,  0};
    float newData_expected[NGATES_10] = {-3,-3, -3, 5, 5, 5, -3,-3,-3, -3}; 

    bool   bnd[NGATES_10] =             { 0, 0,  0, 0, 0, 0,  1, 1, 1,  1};

    float bad_flag = -3;
    size_t a_speckle = 3;
    size_t nGates = NGATES_10;
    size_t clip_gate = nGates;

    se_remove_ac_motion(data, newData, nGates, bad_flag, a_speckle, clip_gate, bnd);
    for (int i=0; i<NGATES_10; i++)
      EXPECT_EQ(newData[i], newData_expected[i]);

  }


  TEST(SoloRemoveAcMotion, no_clipping__speckle__boundary_spans_speckle) {
 
    float data[NGATES_10] =             {-3,-3, -3, 5, 5, 5, -3, 5, 5, -3};
    float newData[NGATES_10] =          { 0, 0,  0, 0, 0, 0,  0, 0, 0,  0};
    float newData_expected[NGATES_10] = {-3,-3, -3,-3,-3,-3, -3, 5, 5, -3}; // 1st speckle zapped

    bool  bnd[NGATES_10] =              { 0, 0,  1, 1, 1, 1,  1, 1, 0,  0};

    float bad_flag = -3;
    size_t a_speckle = 3;
    size_t nGates = NGATES_10;
    size_t clip_gate = nGates;

    se_remove_ac_motion(data, newData, nGates, bad_flag, a_speckle, clip_gate, bnd);
    for (int i=0; i<NGATES_10; i++)
      EXPECT_EQ(newData[i], newData_expected[i]);

  }

  TEST(SoloRemoveAcMotion, clipping__speckle_at_beginning__skip_speckle_at_end__no_boundary) {

    float data[NGATES_7] =             { 5, -3, -3, -3, 5, 5,-3};
    float newData[NGATES_7] =          { 0,  0,  0,  0, 0, 0, 0};
    float newData_expected[NGATES_7] = {-3, -3, -3, -3, 5, 5,-3};

    bool  bnd[NGATES_7] = {1,1,1,1,1,1,1};
    float bad_flag = -3;
    size_t a_speckle = 3;
    size_t nGates = NGATES_7;
    size_t clip_gate = 5;

    se_remove_ac_motion(data, newData, nGates, bad_flag, a_speckle, clip_gate, bnd);
    for (int i=0; i<NGATES_7; i++)
      EXPECT_EQ(newData[i], newData_expected[i]);
  }

  TEST(SoloRemoveAcMotion, speckle_at_boundary_edges_ignored) {
    //                                   b,  g,  g,  b, b, g, g
    float data[NGATES_7] =             {-3,  5,  5, -3,-3, 5, 5};
    float newData[NGATES_7] =          { 0,  0,  0,  0, 0, 0, 0};
    float newData_expected[NGATES_7] = {-3,  5,  5, -3,-3, 5, 5}; // no change

    bool  bnd[NGATES_7] =              { 0,  0,  1,  1, 1, 1, 0};
    float bad_flag = -3;
    size_t a_speckle = 3;
    size_t nGates = NGATES_7;
    size_t clip_gate = 5;

    se_remove_ac_motion(data, newData, nGates, bad_flag, a_speckle, clip_gate, bnd);
    for (int i=0; i<NGATES_7; i++)
      EXPECT_EQ(newData[i], newData_expected[i]);
  }
  */

}  // namespace

