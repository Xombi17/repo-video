import React from "react";
import { AbsoluteFill, Video, staticFile, useVideoConfig } from "remotion";
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import { slide } from "@remotion/transitions/slide";

export const MainComposition: React.FC = () => {
  const { fps } = useVideoConfig();

  return (
    <TransitionSeries>
      {/* Intro Slide (5 seconds) */}
      <TransitionSeries.Sequence durationInFrames={5 * fps}>
        <AbsoluteFill style={{ backgroundColor: "#0f172a", justifyContent: "center", alignItems: "center", color: "white", fontFamily: "sans-serif" }}>
          <h1 style={{ fontSize: "80px", fontWeight: "bold" }}>AI Video Generated with AI</h1>
          <p style={{ fontSize: "30px", opacity: 0.8, marginTop: "20px" }}>Autonomous Video Walkthrough Demonstration</p>
        </AbsoluteFill>
      </TransitionSeries.Sequence>

      {/* Slide transition overlay */}
      <TransitionSeries.Transition
        presentation={slide({ direction: "from-right" })}
        timing={linearTiming({ durationInFrames: 15 })}
      />

      {/* Walkthrough Video (Sequences the generated video) */}
      <TransitionSeries.Sequence durationInFrames={55 * fps}>
        <AbsoluteFill style={{ backgroundColor: "black" }}>
          {/* Ensure the output stitched video is copied to the public folder */}
          <Video src={staticFile("walkthrough.mp4")} style={{ width: "100%", height: "100%" }} />
        </AbsoluteFill>
      </TransitionSeries.Sequence>
    </TransitionSeries>
  );
};
