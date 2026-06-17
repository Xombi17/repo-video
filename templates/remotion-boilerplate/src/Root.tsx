import React from "react";
import { Composition } from "remotion";
import { MainComposition } from "./Composition";

export const Root: React.FC = () => {
  return (
    <>
      <Composition
        id="MainComposition"
        component={MainComposition}
        durationInFrames={1800} // Default 60 seconds at 30fps
        fps={30}
        width={1920}
        height={1080}
      />
    </>
  );
};
