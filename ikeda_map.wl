(* ::Package:: *)

ikeda[{x_, y_}, u_] := Module[{t},
  t = 0.4 - 6/(1 + x^2 + y^2);
  {
    1 + u (x Cos[t] - y Sin[t]),
    u (x Sin[t] + y Cos[t])
  }
];

trajectory[u_, steps_: 50000, discard_: 1000] := 
  NestList[ikeda[#, u] &, {0., 0.}, steps] // 
    Drop[#, discard] &;

Manipulate[
  ListPlot[
    trajectory[u, 20000, 1000],
    PlotStyle -> Black,
    PlotRange -> {{-4, 4}, {-4, 4}},
    AspectRatio -> 1,
    Axes -> False,
    Frame -> True,
    PlotLabel -> Row[{"ikeda attractor, u = ", NumberForm[u, {3, 3}]}]
  ],
  {{u, 0.7, "u"}, 0.6, 1, 0.001},
  ControlPlacement -> Top
]
