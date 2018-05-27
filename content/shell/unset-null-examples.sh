#!/usr/bin/env bash

echo; echo 'unset FOO'; unset FOO
printf 'echo %-11s%s%s\n' '${FOO-bar}'  '  # ' "${FOO-bar}"
printf 'echo %-11s%s%s\n' '${FOO?bar}'  '  # ' "(cause an error)"
printf 'echo %-11s%s%s\n' '${FOO+bar}'  '  # '  "(unset value of FOO)"
printf 'echo %-11s%s%s\n' '${FOO:-bar}' '  # ' "${FOO:-bar}"
printf 'echo %-11s%s%s\n' '${FOO:?bar}' '  # ' "(cause an error)"
printf 'echo %-11s%s%s\n' '${FOO:+bar}' '  # ' "(unset value of FOO)"
echo 'unset FOO'; unset FOO
printf 'echo %-11s%s%s\n' '${FOO=bar}'  '  # ' "${FOO=bar}"
printf 'echo %-11s%s%s\n' '${FOO}'      '  # ' "${FOO}"
echo 'unset FOO'; unset FOO
printf 'echo %-11s%s%s\n' '${FOO:=bar}' '  # ' "${FOO:=bar}"
printf 'echo %-11s%s%s\n' '${FOO}'      '  # ' "${FOO}"

echo

echo; echo 'FOO='; FOO=
printf 'echo %-11s%s%s\n' '${FOO-bar}'  '  # ' "(null value of FOO)"
printf 'echo %-11s%s%s\n' '${FOO?bar}'  '  # ' "(null value of FOO)"
printf 'echo %-11s%s%s\n' '${FOO+bar}'  '  # ' "${FOO+bar}"
printf 'echo %-11s%s%s\n' '${FOO:-bar}' '  # ' "${FOO:-bar}"
printf 'echo %-11s%s%s\n' '${FOO:?bar}' '  # ' "(cause an error)"
printf 'echo %-11s%s%s\n' '${FOO:+bar}' '  # '  "(null value of FOO)"
echo 'FOO='; FOO=
printf 'echo %-11s%s%s\n' '${FOO=bar}'  '  # ' "(null value of FOO)"
printf 'echo %-11s%s%s\n' '${FOO}'      '  # ' "(null value of FOO)"
echo 'FOO='; FOO=
printf 'echo %-11s%s%s\n' '${FOO:=bar}' '  # ' "${FOO:=bar}"
printf 'echo %-11s%s%s\n' '${FOO}'      '  # ' "${FOO}"

echo

echo; echo 'FOO=foo'; FOO=foo
printf 'echo %-11s%s%s\n' '${FOO-bar}'  '  # ' "${FOO-bar}"
printf 'echo %-11s%s%s\n' '${FOO?bar}'  '  # ' "${FOO?bar}"
printf 'echo %-11s%s%s\n' '${FOO+bar}'  '  # ' "${FOO+bar}"
printf 'echo %-11s%s%s\n' '${FOO:-bar}' '  # ' "${FOO:-bar}"
printf 'echo %-11s%s%s\n' '${FOO:?bar}' '  # ' "${FOO:?bar}"
printf 'echo %-11s%s%s\n' '${FOO:+bar}' '  # ' "${FOO:+bar}"
echo 'FOO=foo'; FOO=foo
printf 'echo %-11s%s%s\n' '${FOO=bar}'  '  # ' "${FOO=bar}"
printf 'echo %-11s%s%s\n' '${FOO}'      '  # ' "${FOO}"
echo 'FOO=foo'; FOO=foo
printf 'echo %-11s%s%s\n' '${FOO:=bar}' '  # ' "${FOO:=bar}"
printf 'echo %-11s%s%s\n' '${FOO}'      '  # ' "${FOO}"
