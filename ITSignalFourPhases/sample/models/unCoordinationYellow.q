strategy Opt =minE (totalwaitingVehicles) [<=120]: <> yellow.End
simulate 1[<=100] { 2*yellow.North + 4*yellow.East + 6* yellow.South + 8*yellow.West } under Opt

