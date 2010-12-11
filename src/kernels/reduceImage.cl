inline long indexFromImagePosition(int2 imgpos, uint width, uint height, uint buckets, uint currentBucket)
{
    return currentBucket + (imgpos.x * buckets) + (imgpos.y * width * buckets);
}

__kernel void reduceImage(__global uchar * input, __global uchar * output, __global uchar * q, uint width, uint height, uint buckets)
{
    int gid = get_global_id(0);
    int2 imgpos = {0, 0};

    imgpos.x = gid % width;
    imgpos.y = floor((float)gid / (float)width);

    q[gid] = output[gid] = 0;

    long btot = 0;

    for(uint i = 0; i < buckets; i++)
    {
        uchar bval = input[indexFromImagePosition(imgpos, width, height, buckets, i)];

        btot += bval;

        if(bval > q[gid])
        {
            q[gid] = bval;
            output[gid] = i;
        }
    }

    output[gid] = (output[gid] + 1);

    if(!(btot > (1.0 * q[gid])))
    {
        output[gid] = q[gid] = 0;
    }
}
