
# Stable Diffusion URL路徑
sd_url = "http://127.0.0.1:7860"
sd_txt2img_api_url = sd_url + "/sdapi/v1/txt2img"
sd_checkpoints_url = sd_url + "/sdapi/v1/sd-models"
sd_current_checkpoint_url = sd_url + "/sdapi/v1/options"

# Stable Diffusion 檔案路徑
sd_base_path = "../sd_web/"
sd_web_path = sd_base_path + "webui/"
sd_launch_path = sd_web_path + "launch.py"

# 分析檔案儲存路徑
data_base_path = "./image_datas/"
prompt_data_path = data_base_path + "prompt_list.txt"
image_info_path = data_base_path + "image_data_info/"
image_file_path = data_base_path + "image_data_file/"

#------------------------------------------------------------------------------
# 影像分析模型檔案路徑
analysiser_base_path = "./analysisers_data/"
analysiser_list_file_path =  analysiser_base_path + "analysiser_list.txt"

#------------------------------------------------------------------------------
display_image_width = 300
display_image_height = 300
display_image_wh_rate = display_image_width/display_image_height