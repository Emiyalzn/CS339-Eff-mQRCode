import os

import numpy as np

from options.test_options import TestOptions
from data import CreateDataLoader
from models import create_model
from util.visualizer import save_images
from util import html
import time

if __name__ == '__main__':
    opt = TestOptions().parse()
    # hard-code some parameters for test
    opt.num_threads = 1 # test code only supports num_threads = 1
    opt.batch_size = 1 # test code only supports batch_size = 1
    opt.serial_batches = True # no shuffle
    opt.no_flip = True # no flip
    opt.display_id = -1 # no visdom display

    data_loader = CreateDataLoader(opt)
    dataset = data_loader.load_data()
    model = create_model(opt)
    model.setup(opt)
    # create a webpage
    web_dir = os.path.join(opt.results_dir, opt.name, '%s_%s' % (opt.phase, opt.epoch))
    webpage = html.HTML(web_dir, 'Experiment = %s, Phase = %s, Epoch = %s' % (opt.name, opt.phase, opt.epoch))

    # pix2pix: we use batchnorm and dropout in the original pix2pix. You can experiment it with and without eval() mode.
    if opt.eval:
        model.eval()
    eval_times = np.zeros(len(dataset))
    for i, data in enumerate(dataset):
        if i >= opt.num_test:
            break
        start = time.time()
        model.set_input(data)
        model.test()
        end = time.time()
        eval_times[i] = end - start
        visuals = model.get_current_visuals()
        img_path = model.get_image_paths()
        if i % 5 == 0:
            print('processing (%04d)-th image... %s' % (i, img_path))
        save_images(webpage, visuals, img_path, aspect_ratio=opt.aspect_ratio, width=opt.display_winsize)

    time_mean = np.mean(eval_times)
    time_std = np.std(eval_times)

    print(f"Statistic of processing time: \n mean: {time_mean:.3f}. \n std: {time_std:.3f}.")

    # save the webpage
    webpage.save()