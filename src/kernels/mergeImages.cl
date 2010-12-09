inline int indexFromImagePosition(int2 imgpos, uint width, uint height, uint buckets, uint currentBucket)
{
    return currentBucket + (imgpos.x * buckets) + (imgpos.y * width * buckets);
}

__kernel void mergeImages(__global uchar * input, __global uchar * output, uint width, uint height, uint buckets, uint currentBucket)
{
    int gid = get_global_id(0);
    int2 imgpos = {0, 0};

    imgpos.x = gid % width;
    imgpos.y = floor((float)gid / (float)width);

    output[indexFromImagePosition(imgpos, width, height, buckets, currentBucket)] = input[gid];
}
