#pragma once
#include "Trajectory.h"

namespace xmol::trajectory {

template<typename TrajectoryPreprocessor>
class PreprocessedTrajectory {
public:
  TrajectoryPreprocessor(){}

private:
  Trajectory& traj;
  TrajectoryPreprocessor preprocessor;
};

} // namespace xmol::trajectory
