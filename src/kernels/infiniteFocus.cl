__kernel void infiniteFocus(__global uchar * input, __global uchar * output, __global uchar * depth, uint width, uint height, uint buckets, uint currentBucket)
{
    int gid = get_global_id(0);
    int2 imgpos = {0, 0};

    if(depth[gid] == (currentBucket + 1))
    {
        output[gid] = input[gid];
    }
}
