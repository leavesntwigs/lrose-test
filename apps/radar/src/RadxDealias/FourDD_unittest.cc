
#include "FourDD.hh"
#include "gtest/gtest.h"

namespace {

  // TODO: consider making a constructor with most of
  // these parameters set to default values
  /*
  FourDD fourDD(bool debug,
		char *sounding_url,
		float sounding_look_back,
		float wind_alt_min,
		float wind_alt_max,
		float avg_wind_u,
		float avg_wind_v,
		bool prep,
		bool filt,
		bool output_soundVol,
		float max_shear,
		int sign,
		int del_num_bins,
		bool no_dbz_rm_rv,
		float low_dbz,
		float high_dbz,
		float angle_variance,
		float comp_thresh,
		float comp_thresh2,
		bool strict_first_pass,
		int max_count,
		float ck_val,
		int proximity,
		int min_good,
		float std_thresh,
		float epsilon);
  */

  int maxSweeps_simple = 1;
  Volume *velocity = Rsl::new_volume(maxSweeps_simple);
  Volume *lastVolume = Rsl::new_volume(maxSweeps_simple);
  Volume *soundVolume = Rsl::new_volume(maxSweeps_simple);

  /*
  TEST(FourDD, InitialDealiasing_EverythingWorks) {
    FourDD fourDD;
    int maxSweeps = 1;
    Volume *velocity = Rsl::new_volume(maxSweeps);
    velocity->h.missing = -9.0;
    fourDD.InitialDealiasing();
    //    EXPECT_EQ(-9.0, fourDD.getMissingValue(velocity));
  }

  TEST(FourDD, InitialDealiasing_FirstPassSpatialContinuity_AllMissing) {
    FourDD fourDD;
    int maxSweeps = 1;
    Volume *velocity = Rsl::new_volume(maxSweeps);
    velocity->h.missing = -9.0;
    // TODO: make copy of velocity to original
    fourDD.FirstPassSpatialContinuity(STATE, original, velocity,  sweepIndex, del_num_bins, pfraction);
    //    EXPECT_EQ(-9.0, fourDD.getMissingValue(velocity));
  }

  TEST(FourDD, InitialDealiasing_FirstPassSpatialContinuity_NoMissing) {
    FourDD fourDD;
    int maxSweeps = 1;
    Volume *velocity = Rsl::new_volume(maxSweeps);
    velocity->h.missing = -9.0;
    // TODO: make copy of velocity to original
    fourDD.FirstPassSpatialContinuity(STATE, original, velocity,  sweepIndex, del_num_bins, pfraction);
    //    EXPECT_EQ(-9.0, fourDD.getMissingValue(velocity));
  }

  TEST(FourDD, InitialDealiasing_UnfoldUsingWindow) {
    FourDD fourDD;
    int maxSweeps = 1;
    Volume *velocity = Rsl::new_volume(maxSweeps);
    velocity->h.missing = -9.0;
    // TODO: make copy of velocity to original
    fourDD.UnfoldRemoteBinsOrUnsuccessfulBinsUsingWindow(
	       STATE, original, velocity,  sweepIndex, del_num_bins, pfraction);
    //    EXPECT_EQ(-9.0, fourDD.getMissingValue(velocity));
  }


  TEST(FourDD, InitialDealiasing_SecondPassSoundVolumeOnly) {
    FourDD fourDD;
    int maxSweeps = 1;
    Volume *velocity = Rsl::new_volume(maxSweeps);
    velocity->h.missing = -9.0;
    // TODO: make copy of velocity to original
    fourDD.SecondPassSoundVolumeOnly(STATE, original, velocity,  sweepIndex, del_num_bins, fraction2, pfraction);
    //    EXPECT_EQ(-9.0, fourDD.getMissingValue(velocity));
  }

  */
  TEST(FourDD, Unfold_negative) {
    FourDD fourDD;
    int maxSweeps = 1;
    Volume *velocity = Rsl::new_volume(maxSweeps);
    float foldedValue = 8;
    float referenceValue = -19;
    int max_count = 3;
    float NyqVelocity = 8;
    EXPECT_EQ(-24.0, fourDD.Unfold(foldedValue, referenceValue, max_count, NyqVelocity));
  }

  TEST(FourDD, Unfold_positive) {
    FourDD fourDD;
    int maxSweeps = 1;
    Volume *velocity = Rsl::new_volume(maxSweeps);
    float foldedValue = -3;
    float referenceValue = 23;
    int max_count = 3;
    float NyqVelocity = 8;
    EXPECT_EQ(29.0, fourDD.Unfold(foldedValue, referenceValue, max_count, NyqVelocity));
  }

  TEST(FourDD, Unfold_max_count_exceeded) {
    FourDD fourDD;
    int maxSweeps = 1;
    Volume *velocity = Rsl::new_volume(maxSweeps);
    float foldedValue = 8;
    float referenceValue = -19;
    int max_count = 1;
    float NyqVelocity = 8;
    EXPECT_EQ(-8.0, fourDD.Unfold(foldedValue, referenceValue, max_count, NyqVelocity));
  }

  TEST(FourDD, Unfold_max_count_0) {
    FourDD fourDD;
    int maxSweeps = 1;
    Volume *velocity = Rsl::new_volume(maxSweeps);
    float foldedValue = 2;
    float referenceValue = -19;
    int max_count = 0;
    float NyqVelocity = 8;
    EXPECT_EQ(2.0, fourDD.Unfold(foldedValue, referenceValue, max_count, NyqVelocity));
  }



  TEST(FourDD, getMissingValue) {
    FourDD fourDD;
    int maxSweeps = 1;
    Volume *velocity = Rsl::new_volume(maxSweeps);
    velocity->h.missing = -9.0;
    EXPECT_EQ(-9.0, fourDD.getMissingValue(velocity));
  }

  /*
  // expect an exception here ...
  TEST(FourDD, getMissingValue_NULL) {
    FourDD fourDD;
    Volume *vel = NULL;
    EXPECT_EQ(-9.0, fourDD.getMissingValue(vel));
  }


  TEST(FourDD, findRay_NULL) {
    FourDD fourDD;
    Volume *velocity = NULL;
    velocity->h.missing = -9.0;
    EXPECT_EQ(-9.0, fourDD.findRay(velocity, velocity, 0, 0, 0));
  }

  TEST(FourDD, Filter3x3_NULL) {
    FourDD fourDD;
    float missingVal = -999e+33;
    Volume *velocity = NULL;
    velocity->h.missing = -9.0;
    EXPECT_EQ(-9.0, fourDD.Filter3x3(velocity, 0, missingVal));
  }
  */
  /*
  TEST(FourDD, Filter3x3_binTooBig) {
    FourDD fourDD;
    float missingVal = -999e+33;
    Volume *velocity = simpleVolume;
    velocity->h.missing = missingVal;
    int bin_i = simpleVolume->nbins+1;
    EXPECT_EQ(-9.0, fourDD.Filter3x3(velocity, bin_i, missingVal));
  }

  TEST(FourDD, Filter3x3_binGood) {
    FourDD fourDD;
    float missingVal = -999e+33;
    Volume *velocity = simpleVolume;
    velocity->h.missing = missingVal;
    int bin_i = simpleVolume->nbins-11;
    EXPECT_EQ(-9.0, fourDD.Filter3x3(velocity, bin_i, missingVal));
  }

  TEST(FourDD, AssessNeighborhood_HappyDay) {
    FourDD fourDD;
    float missingVal = -999e+33;
    Volume *velocity = simpleVolume;
    velocity->h.missing = missingVal;
    int bin_i = 1;
    short **STATE;
    int currIndex; 
    int numRays;
    int numberOfDealiasedNeighbors;
    int numberOfTbdNeighbors;
    int binindex[3]; 
    int rayindex[3];

    // TODO: initialize STATE; maybe make this a global variable?

    fourDD.AssessNeighborhood(
              STATE, currIndex, bin_i, numRays,
	      &numberOfDealiasedNeighbors, &numberOfTbdNeighbors,
	      binindex, rayindex);

    EXPECT_EQ(9, numberOfDealiasedNeighbors);
    EXPECT_EQ(9, numberOfTbdNeighbors);
    EXPECT_EQ(9, binindex[0]); // TODO: ...
    EXPECT_EQ(9, rayindex[0]);

  }


  TEST(FourDD, window_HappyDay) {
    FourDD fourDD;
    float missingVal = -999e+33;
    Volume *rvVolume = simpleVolume;
    velocity->h.missing = missingVal;
    int bin_i = simpleVolume->maxBins-11;
    
    int sweepIndex;
    int startray;
    int endray;
    int firstbin;
    int lastbin;
    float std;
    float missingVal; 
    unsigned short success;

    EXPECT_EQ(-9.0, fourDD.window(rvVolume, sweepIndex, startray,
	  endray, firstbin, lastbin, std,
	  missingVal, &success));

  }
  */


} // namespace
