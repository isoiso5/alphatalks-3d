import React from 'react';
import { Composition } from 'remotion';
import { Story3D, StoryProps, defaultStory } from './Story3D';

const FPS = 30;

const totalFrames = (p: StoryProps) =>
  Math.max(1, Math.round(p.scenes.reduce((s, sc) => s + sc.durationSec, 0) * FPS));

export const RemotionRoot: React.FC = () => (
  <>
    {/* Long video 16:9 */}
    <Composition
      id="Story3D"
      component={Story3D}
      fps={FPS}
      width={1920}
      height={1080}
      durationInFrames={totalFrames(defaultStory)}
      defaultProps={defaultStory}
      calculateMetadata={({ props }) => ({ durationInFrames: totalFrames(props) })}
    />
    {/* Short 9:16 */}
    <Composition
      id="Story3DShort"
      component={Story3D}
      fps={FPS}
      width={1080}
      height={1920}
      durationInFrames={totalFrames(defaultStory)}
      defaultProps={defaultStory}
      calculateMetadata={({ props }) => ({ durationInFrames: totalFrames(props) })}
    />
  </>
);
