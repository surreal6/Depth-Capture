import os

path = "/home/carlos/Escritorio/test_mesh/1422053556/"

for file in os.listdir(path):
	output = file.rpartition(".")[0]+"_.ply"
	command = """meshlabserver -i {} -o {} -s ~/Dropbox/sketchbook/Depth-Capture/marching_cubes.mlx -om vc vn"""
	command = command.format(os.path.join(path,file), os.path.join(path, output))
	print(command)
	os.system(command)