import concurrent.futures
from tqdm import tqdm

#=============================================================#
# 接口                                                        #
#-------------------------------------------------------------#
#   multi_process_exec 多进程执行                             #
#   multi_thread_exec  多线程执行                             #
#-------------------------------------------------------------#
# 参数：                                                      #
#   f         (function): 批量执行的函数                      #
#   args_mat  (list)    : 批量执行的参数                      #
#   pool_size (int)     : 进程/线程池的大小                   #
#   desc      (str)     : 进度条的描述文字                    #
#-------------------------------------------------------------#
# 例子：                                                      #
# >>> def Pow(a,n):        ← 定义一个函数（可以有多个参数）   #
# ...     return a**n                                         #
# >>>                                                         #
# >>> args_mat=[[2,1],     ← 批量计算 Pow(2,1)                #
# ...           [2,2],                Pow(2,2)                #
# ...           [2,3],                Pow(2,3)                #
# ...           [2,4],                Pow(2,4)                #
# ...           [2,5],                Pow(2,5)                #
# ...           [2,6]]                Pow(2,6)                #
# >>>                                                         #
# >>> results=multi_thread_exec(Pow,args_mat,desc='计算中')   #
# 计算中: 100%|█████████████| 6/6 [00:00<00:00, 20610.83it/s] #
# >>>                                                         #
# >>> print(results)                                          #
# [2, 4, 8, 16, 32, 64]                                       #
#-------------------------------------------------------------#


ToBatch = lambda arr,size:[arr[i*size:(i+1)*size] for i in range((size-1+len(arr))//size)]

def batch_exec(f,args_batch,w):
    results=[]
    for i,args in enumerate(args_batch):
        try:
            ans = f(*args)
            results.append(ans)
        except Exception:
            results.append(None)
        w.send(1)
    return results

'''
f         (function): 批量执行的函数                      
args_mat  (list)    : 批量执行的参数，函数接收多个传参                   
pool_size (int)     : 进程/线程池的大小                   
desc      (str)     : 进度条的描述文字   
'''
def multi_thread_exec_multi_args(f,args_mat,pool_size=5,desc=None):
    if len(args_mat)==0:return []
    results=[None for _ in range(len(args_mat))]
    with tqdm(total=len(args_mat), desc=desc) as pbar:
        with concurrent.futures.ThreadPoolExecutor(max_workers=pool_size) as executor:
            futures = {executor.submit(f,*args): i for i,args in enumerate(args_mat)}
            for future in concurrent.futures.as_completed(futures):
                i=futures[future]
                ret = future.result()
                results[i]=ret
                pbar.update(1)
    return results

'''
f         (function): 批量执行的函数                      
args_mat  (list)    : 批量执行的参数，函数接收单个传参                   
pool_size (int)     : 进程/线程池的大小                   
desc      (str)     : 进度条的描述文字   
'''
def multi_thread_exec(f,args_mat,pool_size=5,desc=None):
    if len(args_mat)==0:return []
    results=[None for _ in range(len(args_mat))]
    with tqdm(total=len(args_mat), desc=desc) as pbar:
        with concurrent.futures.ThreadPoolExecutor(max_workers=pool_size) as executor:
            futures = {executor.submit(f,args): i for i,args in enumerate(args_mat)}
            for future in concurrent.futures.as_completed(futures):
                i=futures[future]
                ret = future.result()
                results[i]=ret
                pbar.update(1)
    return results


def Pow(a,n):
    return a**n

def Pow1(a):
    return a**2

if __name__=='__main__':
    args_mat=[i for i in range(100)]
    results=multi_thread_exec(Pow1,args_mat,3,desc='多线程单传参')
    print(results)


    args_mat=[(i,2) for i in range(100)]
    results=multi_thread_exec_multi_args(Pow,args_mat,3,desc='多线程多传参')
    print(results)