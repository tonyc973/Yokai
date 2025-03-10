#include <print>
#include "../includes/mymath.h"

int main() {
    int a = 5;
    int b = 2;

    std::println("Res={}", mydiv(a, b).value_or(0));

    return 0;
}

