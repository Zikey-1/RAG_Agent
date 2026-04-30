import numpy as np
# 计算点积
def get_dot(vec_a,vec_b):
    if len(vec_a) != len(vec_b):
        raise ValueError("向量维度不一致")
    
    dot_sum=0
    for a,b in zip(vec_a,vec_b):
        dot_sum += a * b
    return dot_sum


def get_norm(vec):
    sum_squre=0
    for v in vec:
        sum_squre += v ** 2  # 计算单个向量模长
    return np.sqrt(sum_squre)

def cosine_similarity(vec_a,vec_b):
    result = get_dot(vec_a,vec_b) / (get_norm(vec_a) * get_norm(vec_b))
    return result

if __name__ == "__main__":
    vec_a = [0.5,0.5]
    vec_b = [0.7,0.7]
    vec_c = np.array([0.7,0.5])
    vec_d = np.array([-0.6,-0.5])
    print(cosine_similarity(vec_a,vec_b))
    print(cosine_similarity(vec_a,vec_c))
    print(cosine_similarity(vec_a,vec_d))