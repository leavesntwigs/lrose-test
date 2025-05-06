dtm_file='IHOP_DTM_1km '
idtmfile=3
#
ndtmfile=0
if(idtmfile != 0):
   while dtm_file[ndtmfile:ndtmfile+1] != ' ':
      ndtmfile=ndtmfile+1

print("ndtmfile: ", ndtmfile)
print("idtmfile: ", idtmfile)
print("dtm_file: ", dtm_file)
print("len(dtm_file): ", len(dtm_file))
