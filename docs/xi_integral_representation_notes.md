# xi_integral_representation_notes.md (RECOVERED)

Transcribed from Darryl's recovered source document. This is the actual
content the `theta_one_sided_factor` candidate's evidence_files pointed to
by filename only, before the Manus loss. Recovering it unblocks
`paired_theta_hermite_biehler`, which needs this exact kernel to build a
consistent companion E*.

## Canonical theta representation

A standard theta transformation supplies a rapidly decaying real kernel Phi
with

    Xi(t) = 4 * integral_0^infty Phi(u) cos(tu) du,

where

    Phi(u) = Sum_{n>=1} (4*pi^2*n^4*exp(9u/2) - 6*pi*n^2*exp(5u/2)) * exp(-pi*n^2*exp(2u)).

This representation is arithmetic and zero-free in its definition. Phi is
defined on u >= 0 only -- it is NOT itself even, and any even extension must
be specified separately. (Note: an earlier, unrecovered version of this
session's notes guessed coefficients 2*pi^2 and 3*pi -- those were wrong,
never presented as fact, and are superseded by the actual 4*pi^2 / 6*pi
coefficients above, now confirmed from source.)

## Theta-derived one-sided factor

    E_-(z) = 2 * integral_0^infty Phi(u) * exp(-izu) du.

Phi decays super-exponentially, so E_- is entire (locally uniform convergence
on compact subsets of C). Since Phi is real,

    E_-^#(z) := conjugate(E_-(conjugate(z))) = E_-(-z).

Write E_-(z) = A(z) - iB(z). Then

    A(z) = 2 * integral_0^infty Phi(u) cos(zu) du,
    B(z) = 2 * integral_0^infty Phi(u) sin(zu) du,

and therefore, exactly:

    A(z) = Xi(z) / 2.

## The Hermite-Biehler condition (the actual open question)

    |E_-^#(z)| < |E_-(z)|   for Im(z) > 0

would, via the de Branges theorem, imply the zeros of A = Xi/2 are real,
i.e. RH. The CONVERSE -- RH implying E_- is Hermite-Biehler -- has not been
established. Do not conflate:

    E_- Hermite-Biehler => RH

with the unresolved converse, or with a proof that E_- actually is
Hermite-Biehler.

## Exact Wronskian identity (why the scalar version failed)

    W(x) = A(x)B'(x) - A'(x)B(x)
         = 2 * integral_0^infty integral_0^infty (u+v) Phi(u) Phi(v) cos(x(u-v)) du dv.

Certified (Arb, 180-bit, 200000 subdivisions, 5 theta summands):

    W(20) in [-8.25011781628766e-6, -2.42009354494050e-6]

-- a certified strict negative interval. This rules out the DIRECT SCALAR
single-vector positive-unitary correlation (see proof_scalar_theta_weil_bridge_nogo.md
summary on theta_one_sided_factor's record) but does NOT itself resolve
Hermite-Biehler for E_-, and does NOT rule out a genuine paired (E, E*)
Hermite-Biehler construction -- which is exactly what
paired_theta_hermite_biehler proposes to test.

## What paired_theta_hermite_biehler still needs to define

E_- above already gives a natural E* candidate: E*(z) := E_-^#(z) = E_-(-z).
The actual Hermite-Biehler test is |E*(z)| < |E_-(z)| for Im(z) > 0, which is
NOT the same statement as the Wronskian sign test above (the Wronskian
identity concerns A, B on the real line; Hermite-Biehler concerns |E_-| vs
|E*| off the real line). This has not yet been tested numerically in any
recovered document. Recommended first computation: evaluate both sides on a
grid in the upper half-plane near z=20+iy for small y>0, using the same
5-term-plus-tail Phi truncation and Arb precision already validated for the
Wronskian, and check the inequality directly rather than assuming it inherits
the Wronskian's sign.
