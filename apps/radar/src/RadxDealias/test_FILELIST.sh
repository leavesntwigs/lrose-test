#!/bin/sh

~/git/lrose-core/codebase/apps/radar/src/RadxDealias/RadxDealias -f output/20150626/cfrad.20150626_002*.nc -params RadxDealias.params

diff output_dealiased/20150626/cfrad.20150626_002*.nc output_dealiased/20150626/expected/cfrad.20150626_002*nc
# diff output_dealiased/20150626/cfrad.20150626_003*.nc output_dealiased/20150626/expected/cfrad.20150626_003*nc
# diff output_dealiased/20150626/cfrad.20150626_004*.nc output_dealiased/20150626/expected/cfrad.20150626_004*nc
# diff output_dealiased/20150626/cfrad.20150626_005*.nc output_dealiased/20150626/expected/cfrad.20150626_005*nc

ls -lrt output_dealiased/20150626/
ls -lrt output_dealiased/20150626/expected/
