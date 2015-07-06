int X(int a)
{
    if (a<=0) // 1 vez
        return 0; // nao sera executado no pior caso
    int tmp = 0; // 1 vez
    for (i = 1; i<a;i++) // a vezes
    {
        tmp += i; // a -1 vezes
    }
    return tmp; // 1 vez
}
