import os
import hive
import fnmatch

render_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "render")


def get_blend_file(folder_name):
    for root, dirs, files in os.walk(os.path.join(render_path, folder_name)):
        for name in files:
            if fnmatch.fnmatch(name, "*.blend"):
                return os.path.join(root, name)




def render_hive(folder_name):

    # Turning off miner to save on GPU recources
    if hive.check() == True:
        hive.toggle()

    # Making output directory
    output_dir = os.path.join(render_path, folder_name, "output")
    os.system(f"mkdir -p {output_dir} > /dev/null 2>&1")
    
    # Starting to render
    os.system(f"blender -b {get_blend_file(folder_name)} -o {output_dir} -E CYCLES -a -- -cycles-device CUDA+OPENCL+CPU > /dev/null 2>&1")

    #Turning miner back on
    if hive.check() == False:
        hive.toggle()

        
def render(folder_name):
    # Making output directory
    output_dir = os.path.join(render_path, folder_name, "output")
    os.system(f"mkdir -p {output_dir} > /dev/null 2>&1")
    

    # Starting to render
    os.system(f"blender -b {get_blend_file(folder_name)} -o {output_dir} -E CYCLES -a -- -cycles-device CUDA+OPENCL+CPU > /dev/null 2>&1")