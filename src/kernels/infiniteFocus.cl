__kernel void infiniteFocus(__global uchar * input, __global uchar * output, __global uchar * depth, uint currentBucket)
{
    int gid = get_global_id(0);

    if(depth[gid] == (currentBucket + 1))
    {
        output[gid] = input[gid];
    }
}
