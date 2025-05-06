
FROM ubuntu:22.04



# ADD . /tmp/bj
# WORKDIR /tmp/bj

#
#
#   - run:
#           name: install packages
#           command: |
#             sudo apt-get update
#             sudo apt-get install -y gcc gfortran libnetcdf-dev libnetcdff-dev libhdf5-dev hdf5-tools
#             
#      - run: git clone https://github.com/mmbell/Airborne-Radar-QC.git
#      #             find / -name netcdf.inc
#      #             find / -name libhdf5*
#      - run: 
#          name: build the code
#          command: |
#            pwd
#            ls 
#            cd Airborne-Radar-QC/navigation
#            gfortran -g  -o readnetcdf_DBZ_VR  -fallow-argument-mismatch -fallow-invalid-boz readnetcdf_DBZ_VR.f90 -I/usr/include -L/usr/local/lib -lnetcdf -lnetcdff -lcurl -L/usr/lib/x86_64-linux-gnu/hdf5/serial -lhdf5 -lhdf5_hl -I/usr/local/include
#            gfortran -g  -o cns_eldo_cai cns_eldo_cai.f chol_inv.f -fallow-argument-mismatch -fallow-invalid-boz -I/usr/include -L/usr/local/lib -lnetcdf -lnetcdff -lcurl -L/usr/lib/x86_64-linux-gnu/hdf5/serial -lhdf5 -lhdf5_hl -I/usr/local/include

RUN apt-get update &&  apt-get install -y  gcc gfortran libnetcdf-dev libnetcdff-dev libhdf5-dev hdf5-tools git vim

# RUN git clone https://github.com/mmbell/Airborne-Radar-QC.git
# RUN pwd
# RUN ls
# RUN cd Airborne-Radar-QC/navigation
# RUN gfortran -g  -o readnetcdf_DBZ_VR  -fallow-argument-mismatch -fallow-invalid-boz readnetcdf_DBZ_VR.f90 -I/usr/include -L/usr/local/lib -lnetcdf -lnetcdff -lcurl -L/usr/lib/aarch64-linux-gnu/hdf5/serial -lhdf5 -lhdf5_hl -I/usr/local/include
# 
# RUN gfortran -g  -o cns_eldo_cai cns_eldo_cai.f chol_inv.f -fallow-argument-mismatch -fallow-invalid-boz -I/usr/include -L/usr/local/lib -lnetcdf -lnetcdff -lcurl -L/usr/lib/aarch64-linux-gnu/hdf5/serial -lhdf5 -lhdf5_hl -I/usr/local/include 

# create a user
# RUN useradd -ms /bin/bash lrose 
# USER lrose
# WORKDIR /home/lrose


RUN git clone https://github.com/mmbell/Airborne-Radar-QC.git
RUN pwd
RUN ls
# RUN cd ~/Airborne-Radar-QC/navigation; gfortran -g  -o readnetcdf_DBZ_VR  -fallow-argument-mismatch -fallow-invalid-boz readnetcdf_DBZ_VR.f90 -I/usr/include -L/usr/local/lib -lnetcdf -lnetcdff -lcurl -L/usr/lib/aarch64-linux-gnu/hdf5/serial -lhdf5 -lhdf5_hl -I/usr/local/include

##  RUN cd ~/Airborne-Radar-QC/navigation; gfortran -g  -o cns_eldo_cai cns_eldo_cai.f chol_inv.f -fallow-argument-mismatch -fallow-invalid-boz -I/usr/include -L/usr/local/lib -lnetcdf -lnetcdff -lcurl -L/usr/lib/aarch64-linux-gnu/hdf5/serial -lhdf5 -lhdf5_hl -I/usr/local/include 
