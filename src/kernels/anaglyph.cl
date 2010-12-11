inline long indexFromImagePosition(int2 imgpos, uint width, uint height)
{
    return imgpos.x + (imgpos.y * width);
}

__kernel void anaglyph(__global uchar * input, __global uchar * output, __global uchar * depth, uint width, uint height, int direction)
{
    int gid = get_global_id(0);
    size_t gsize = get_global_size(0);

    int2 imgpos = {0, 0};
    int2 mypos;

    imgpos.x = gid % width;
    imgpos.y = floor((float)gid / (float)width);

    mypos = imgpos;

    mypos.x += direction * (depth[gid] * 0.1);
    mypos.x = max(min((float)mypos.x, (float)width), 0.0f);

    long idx = indexFromImagePosition(mypos, width, height);

    if(idx < gsize)
    {
        output[gid] = input[idx];
    }
    else
    {
        output[gid] = input[gid];
    }
}
