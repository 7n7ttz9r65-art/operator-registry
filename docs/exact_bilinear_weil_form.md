# exact_bilinear_weil_form.md (RECOVERED)

Transcribed from Darryl's recovered source document, section 9. Backs
`weil_gaussian_convolution`'s `trace_status: proved`.

## Setup

    f_hat(t) = integral_R exp(itu) f(u) du,
    g_tilde(u) = conjugate(g(-u)).

Let T_W be an admissible analytic test class with sufficient decay and
continuation for pole evaluations, gamma integrals, and explicit-formula
interchanges.

## The Guinand-Weil explicit formula (general, non-even h)

    Sum_rho h_hat(gamma_rho)
      = h_hat(i/2) + h_hat(-i/2)
        + (1/2pi) integral_R [Re psi(1/4 + it/2) - log(pi)] h_hat(t) dt
        - Sum_{n>=2} (Lambda(n)/sqrt(n)) [h(log n) + h(-log n)].

Zeros written as rho = beta_rho + i*gamma_rho, unconditionally. Writing
every zero as 1/2 + i*gamma_rho assumes RH -- not done here.

## The bilinear identity

For h = f * g_tilde (convolution, not pointwise product):

    h_hat(t) = f_hat(t) * conjugate(g_hat(t)),

so, defining Q_W(f,g) := W(f * g_tilde) (W = the right-hand side of the
explicit formula above, evaluated at h = f*g_tilde):

    Q_W(f,g) = Sum_rho f_hat(gamma_rho) * conjugate(g_hat(gamma_rho))   [zero side]
             = [pole] + [archimedean] - [prime]                          [explicit-formula side]

The prime term uses convolution values (f*g_tilde)(+-log n), NOT pointwise
products f(log n)*g(log n) -- this was one of two implementation errors
found and corrected in the source session:

1. The archimedean factor was originally missing its `-log(pi)` term.
2. The pole and prime terms had accidentally been divided by two during an
   earlier symmetrization step.

The corrected implementation (used for `exact_bilinear_weil_gaussian_results.json`,
below) was checked against an independent term-by-term reconstruction and
agreed.

## Instantiated at Gaussian translates

    f_a(u) = exp(-(u-a)^2 / (2*sigma^2)),
    g_tilde_b(u) = exp(-(u+b)^2 / (2*sigma^2)),

    (f_a * g_tilde_b)(x) = sqrt(pi)*sigma * exp(-(x-a+b)^2 / (4*sigma^2)).

This is the exact object numerically evaluated (pole + prime + gamma terms,
each derived above, no pointwise-product shortcut) to produce the eigenvalue
data in `exact_bilinear_weil_gaussian_results.json`.
