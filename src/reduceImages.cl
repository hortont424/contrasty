inline int indexFromImagePosition(int2 imgpos, uint width, uint height)
{
    return imgpos.x + (imgpos.y * width);
}

__kernel void reduceImages(__global uchar * input1, __global uchar * input2, __global uchar * output, uint width, uint height)
{
    int gid = get_global_id(0);
    int2 imgpos = {0, 0};

    imgpos.x = gid % width;
    imgpos.y = floor((float)gid / (float)width);

    /*long total = 0;
    uchar value = input[gid], sample;

    int x = max((int)(imgpos.x - r), (int)0);
    int y = max((int)(imgpos.y - r), (int)0);
    int maxX = min((int)(imgpos.x + r), (int)width);
    int maxY = min((int)(imgpos.y + r), (int)height);

    long totalCount = (maxX - x) + (maxY - y);

    for(; x <= maxX; x++)
    {
        int2 frompos = {x, imgpos.y};

        sample = input[indexFromImagePosition(frompos, width, height)];

        total += abs(sample - value) * gaussian[abs(x - imgpos.x)];
    }

    for(; y <= maxY; y++)
    {
        int2 frompos = {imgpos.x, y};

        sample = input[indexFromImagePosition(frompos, width, height)];

        total += abs(sample - value) * gaussian[abs(y - imgpos.y)];
    }

    output[gid] = (uchar) (((float)total / totalCount) * 5.0);*/

    output[gid] = ((input2[gid] + input1[gid] / 2.0) > 32) ? (input2[gid] > input1[gid] * 1.2 ? 255 : 70) : 0;
}
