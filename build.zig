const std = @import("std");
const OptimizeMode = std.builtin.OptimizeMode;
const ResolvedTarget = std.Build.ResolvedTarget;

const src_files = .{"src/mymath.cpp"};

pub fn build(b: *std.Build) void {
    const target = b.standardTargetOptions(.{});
    const optimize = b.standardOptimizeOption(.{});

    build_exe(b, target, optimize);
    build_tests(b, target, optimize);
    build_docs(b, target, optimize);
}

fn build_exe(
    b: *std.Build,
    target: ResolvedTarget,
    optimize: OptimizeMode,
) void {
    const exe = b.addExecutable(.{
        .name = "yokai",
        .target = target,
        .optimize = optimize,
        .use_llvm = false,
    });

    exe.linkLibCpp();

    exe.addCSourceFiles(.{
        .root = b.path("."),
        .files = &(.{"src/main.cpp"} ++ src_files),
        .flags = &.{
            "-std=c++23",
            "-pedantic",
            "-Werror",
            "-Wall",
            "-Wextra",
        },
    });

    b.installArtifact(exe);

    const run_cmd = b.addRunArtifact(exe);
    run_cmd.step.dependOn(b.getInstallStep());
    if (b.args) |args| {
        run_cmd.addArgs(args);
    }

    const run_step = b.step("run", "Run the app");
    run_step.dependOn(&run_cmd.step);
}

fn build_tests(
    b: *std.Build,
    target: ResolvedTarget,
    optimize: OptimizeMode,
) void {
    const unit_tests = b.addExecutable(.{
        .name = "unit_tests",
        .target = target,
        .optimize = optimize,
        .use_llvm = false,
    });

    unit_tests.linkLibCpp();

    const test_files = .{ "tests/main.cpp", "tests/mydiv_test.cpp" };
    unit_tests.addCSourceFiles(.{
        .root = b.path("."),
        .files = &(src_files ++ test_files),
        .flags = &.{
            "-std=c++23",
            "-pedantic",
            "-Werror",
            "-Wall",
            "-Wextra",
        },
    });

    b.installArtifact(unit_tests);

    const test_cmd = b.addRunArtifact(unit_tests);
    test_cmd.step.dependOn(b.getInstallStep());
    if (b.args) |args| {
        test_cmd.addArgs(args);
    }

    const test_step = b.step("test", "Run unit tests");
    test_step.dependOn(&test_cmd.step);
}

fn build_docs(
    b: *std.Build,
    target: ResolvedTarget,
    optimize: OptimizeMode,
) void {
    const exe = b.addExecutable(.{
        .name = "yokai",
        .target = target,
        .optimize = optimize,
        .use_llvm = false,
    });

    exe.linkLibCpp();

    exe.addCSourceFiles(.{
        .root = b.path("."),
        .files = &(.{"src/main.cpp"} ++ src_files),
        .flags = &.{
            "-std=c++23",
            "-pedantic",
            "-Werror",
            "-Wall",
            "-Wextra",
        },
    });

    b.installArtifact(exe);

    const run_cmd = b.addRunArtifact(exe);
    run_cmd.step.dependOn(b.getInstallStep());
    if (b.args) |args| {
        run_cmd.addArgs(args);
    }

    const run_step = b.step("run", "Run the app");
    run_step.dependOn(&run_cmd.step);
}
