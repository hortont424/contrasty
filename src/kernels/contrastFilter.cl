inline long indexFromImagePosition(int2 imgpos, uint width, uint height)
{
    return imgpos.x + (imgpos.y * width);
}

__kernel void contrastFilter(__global uchar * input, __global uchar * output, __global float * gaussian, uint width, uint height, uint size)
{
    long gid = get_global_id(0);
    size_t gsize = get_global_size(0);

    char r = floor(size * 0.5f);
    int2 imgpos = {0, 0};

    imgpos.x = gid % width;
    imgpos.y = floor((float)gid / (float)width);

    float total = 0;
    uchar value = input[gid], sample;

    int x = max((int)(imgpos.x - r), (int)0);
    int y = max((int)(imgpos.y - r), (int)0);
    int maxX = min((int)(imgpos.x + r), (int)width);
    int maxY = min((int)(imgpos.y + r), (int)height);

    float totalCount = 0;

    float sinvsq = 36.0 / ((1.0 + 2.0 * r) * (1.0 + 2.0 * r));

    for(; x <= maxX; x++)
    {
        for(; y <= maxY; y++)
        {
            int2 frompos = {x, y};
            long index = indexFromImagePosition(frompos, width, height);

            if(index < 0 || index > gsize)
            {
                continue;
            }

            sample = input[index];

            float gval = native_exp((float) -((0.5f * ((x - imgpos.x) * (x - imgpos.x)) * sinvsq) +
                                              (0.5f * ((y - imgpos.y) * (y - imgpos.y)) * sinvsq)));

            total += abs(sample - value) * gval;
            totalCount += gval;
        }
    }

    output[gid] = (uchar) (total / totalCount); // TODO: this is not proper normalization
}
