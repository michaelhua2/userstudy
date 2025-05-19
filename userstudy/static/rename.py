import os
import os.path as osp
import shutil

num_method = 3
cnt = 1
method2id = {'gt': 1,
 'ours_refine': 2,
 'grasptta': 3,
}

data_dir = 'data'
for root,dirs,files in os.walk(osp.join(data_dir, 'gt/')):
    for file in files:
        if(file.endswith('.gif')):
            index = file.split('.gif')[0]
            # tmp = file.split('_')
            # fnum = int(tmp[0])

            # check that files exists for all method
            okay_flag = True
            for method, ind in method2id.items():
                if not os.path.exists(os.path.join(data_dir, method, file)):
                    okay_flag = False
                    print(os.path.join(method, file))
                    break
            if not okay_flag:
                continue

            for method, ind in method2id.items():
                if not os.path.exists(os.path.join(data_dir, str(ind))):
                    os.makedirs(os.path.join(data_dir, str(ind)))
                shutil.copyfile(os.path.join(data_dir, method, file), os.path.join(data_dir, str(ind), str(cnt)+'.gif'))
            # shutil.move(os.path.join('1/',file),os.path.join('1/',str(cnt)+'.png'))
            # shutil.move(os.path.join('2/',file),os.path.join('2/',str(cnt)+'.png'))
            # shutil.move(os.path.join('3/',file),os.path.join('3/',str(cnt)+'.png'))
            cnt += 1
