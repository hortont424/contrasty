inline int indexFromImagePosition(int2 imgpos, uint width, uint height)
{
    return imgpos.x + (imgpos.y * width);
}

__kernel void contrastFilter(__global uchar * input, __global uchar * output, uint width, uint height)
{
    int gid = get_global_id(0);
    char d = 41;
    char r = floor(d / 2.0f);
    int2 imgpos = {0, 0};

    imgpos.x = gid % width;
    imgpos.y = floor((float)gid / (float)width);

    float sinvsq = 36.0f / ((1.0f + 2.0f * r) * (1.0f + 2.0f * r));
    long total = 0;
    uchar value = input[gid], sample;

    int x = max((int)(imgpos.x - r), (int)0);
    int y = max((int)(imgpos.y - r), (int)0);
    int maxX = min((int)(imgpos.x + r), (int)width);
    int maxY = min((int)(imgpos.y + r), (int)height);

    long totalCount = (maxX - x) + (maxY - y);

    float gauss;
    int subindex;
    int2 frompos;

    for(; x <= maxX; x++)
    {
        subindex = x - imgpos.x;
        // TODO: This is really dumb, because the kernel is the same for a given subindex for the whole program
        gauss = native_exp(-0.5f * (subindex * subindex) * sinvsq);
        frompos = imgpos;
        frompos.x = x;

        sample = input[indexFromImagePosition(frompos, width, height)];

        total += abs(sample - value) * gauss;
    }

    for(; y <= maxY; y++)
    {
        subindex = y - imgpos.y;
        gauss = native_exp(-0.5f * (subindex * subindex) * sinvsq);
        frompos = imgpos;
        frompos.y = y;

        sample = input[indexFromImagePosition(frompos, width, height)];

        total += abs(sample - value) * gauss;
    }

    output[gid] = (uchar) (((float)total / totalCount) * 5.0);
}
