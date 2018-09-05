# Kattmann, 05.2018, Python3.6
#
# Requires: .su2 meshes for each zone in current dir
# Optional: gmsh .geo files for each zone seperatly in the dir, the .su2
#           meshes are then created by setting "create_zone_meshes" to 1
# Output: .su2 mesh with multiple zones
#
# TODO create Parser such that mesh names can be parsed via command line
#-------------------------------------------------------------------#
import subprocess
#-------------------------------------------------------------------#
# enter the names of .geo files here, without .geo -ending
geo_files = ['channel_only','top_block_only','bottom_block_only']

# output filename
out_mesh_name = 'multizone.su2'

# mesh dimension
ndim = 2
create_zone_meshes = 1

#-------------------------------------------------------------------#
# Create .su2 meshes out of .geo files with gmsh
if create_zone_meshes:
  for file in geo_files:
    create_mesh = ['gmsh', file+'.geo', '-2', '-f', 'su2', '-saveall', '-o', file+'.su2']
    #create_mesh = 'gmsh ' + file+'.geo' + ' -2' + ' -f' + ' su2' + ' -saveall' + ' -o ' + file+'.su2'
    
    process = subprocess.check_output(create_mesh, stderr=subprocess.STDOUT)
  print("Meshes for each zone created.")

#-------------------------------------------------------------------#
# merge .su2 meshes of all zones to single mesh
nzones = len(geo_files)

with open(out_mesh_name,'w') as out_mesh:
  out_mesh.write('NDIME=' + str(ndim) +  '\n')
  out_mesh.write('NZONE=' + str(nzones) + '\n')

  for idx,file in enumerate(geo_files):
    out_mesh.write('\nIZONE=' + str(idx+1) + '\n\n')
    #input.pipe
    with open(geo_files[idx] + '.su2','r') as in_mesh:
      out_mesh.write(in_mesh.read())

#-------------------------------------------------------------------#
print("Input files:")
for idx,file in enumerate(geo_files): print(str(idx+1) + ". " + file)
print("Multi-zone mesh written to file: " + str(out_mesh_name))

