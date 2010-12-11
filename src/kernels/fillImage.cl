inline long indexFromImagePosition(int2 imgpos, uint width, uint height)
{
    return imgpos.x + (imgpos.y * width);
}

__kernel void fillImage(__global uchar * input, __global uchar * output, uint width, uint height)
{
    int gid = get_global_id(0);
    char d = 21;
    char r = floor(d / 2.0f);
    int2 imgpos = {0, 0};

    imgpos.x = gid % width;
    imgpos.y = floor((float)gid / (float)width);

    int x = max((int)(imgpos.x - r), (int)0);
    int y = max((int)(imgpos.y - r), (int)0);
    int maxX = min((int)(imgpos.x + r), (int)width);
    int maxY = min((int)(imgpos.y + r), (int)height);

    if(input[gid] == 0)
    {
        uchar vals[255];
        uchar maxVal = 0;
        uchar maxIdx = 0;
        uchar sample;

        for(int i = 0; i < 255; i++)
            vals[i] = 0;

        for(; x <= maxX; x++)
        {
            for(; y <= maxY; y++)
            {
                int2 frompos = {x, y};

                sample = input[indexFromImagePosition(frompos, width, height)];

                vals[sample]++;
            }
        }

        for(int i = 1; i < 255; i++)
        {
            if(vals[i] > maxVal)
            {
                maxVal = vals[i];
                maxIdx = i;
            }
        }

        output[gid] = maxIdx;
    }
    else
    {
        output[gid] = input[gid];
    }
}
