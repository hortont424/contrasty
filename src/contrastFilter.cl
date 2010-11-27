inline int indexFromImagePosition(int2 imgpos, uint width, uint height)
{
    return imgpos.x + (imgpos.y * width);
}

__kernel void contrastFilter(__global uchar * input, __global uchar * output, __global float * gaussian, uint width, uint height)
{
    int gid = get_global_id(0);
    char d = 41;
    char r = floor(d / 2.0f);
    int2 imgpos = {0, 0};

    imgpos.x = gid % width;
    imgpos.y = floor((float)gid / (float)width);

    long total = 0;
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

    output[gid] = (uchar) (((float)total / totalCount) * 5.0);
}
