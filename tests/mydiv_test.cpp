#include "../lib/doctest.h"
#include "../includes/mymath.h"

TEST_CASE("Valid mydiv operation") {
    REQUIRE(*mydiv(5, 2) == 2);
}
