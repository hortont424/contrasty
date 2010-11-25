inline int indexFromImagePosition(int2 imgpos, uint width, uint height)
{
    return imgpos.x + (imgpos.y * width);
}

__kernel void contrastFilter(__global uchar * input, __global uchar * output, uint width, uint height)
{
    int gid = get_global_id(0);
    long d = 21;
    long r = floor(d / 2.0f);
    int2 imgpos = {0, 0};

    imgpos.x = gid % width;
    imgpos.y = floor((float)gid / (float)width);

    float s = (1.0f / 3.0f) * r + (1.0f / 6.0f);
    long total = 0, totalCount = 0;
    uchar value = input[gid], sample;

    for(int x = -r; x <= r; x++)
    {
        float gauss = exp(-0.5f * (x * x) / (s * s));
        int2 frompos = imgpos;
        frompos.x += x;

        if(frompos.x >= 0 && frompos.x < width)
        {
            sample = input[indexFromImagePosition(frompos, width, height)];

            total += abs(sample - value) * gauss;
            totalCount++;
        }
    }

    output[gid] = (uchar) (total / totalCount) * 2;
}
