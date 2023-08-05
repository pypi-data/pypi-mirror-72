# Set up anaconda environment
ml Anaconda2/4.4.0

# Activate
source activate /data/mcr/anaconda/dax/ldax_v2

# Set PATH
#export PATH=/data/mcr/dax_new/bin/dax_tools:/data/mcr/dax_new/bin/old_tools:/data/mcr/dax_new/bin/freesurfer_tools:/data/mcr/dax_new/bin/Xnat_tools:/data/mcr/masimatlab/trunk/xnatspiders/python/justinlib_v1_1_0/pythonlib/:/data/mcr/masimatlab/trunk/xnatspiders/python/justinlib_v1_1_0/xnatlib/:$PATH
export PATH=/data/mcr/masimatlab/trunk/xnatspiders/python/justinlib_v1_1_0/pythonlib/:/data/mcr/masimatlab/trunk/xnatspiders/python/justinlib_v1_1_0/xnatlib/:$PATH


# Dax modules require matlab
ml MATLAB/2017a

