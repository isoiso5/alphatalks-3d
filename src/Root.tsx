import React from 'react';
import { Composition, Still } from 'remotion';
import { Story3D, Thumbnail, FPS, totalFrames } from './Story3D';
import { StoryProps } from './types';
import sample from './sample.json';

const defaults = sample as unknown as StoryProps;
const meta = ({ props }: { props: StoryProps }) => ({ durationInFrames: Math.max(1, totalFrames(props)) });

export const RemotionRoot: React.FC = () => (
  <>
    {/* Long video 16:9 */}
    <Composition id="Story3D" component={Story3D} fps={FPS} width={1920} height={1080} durationInFrames={totalFrames(defaults)} defaultProps={defaults} calculateMetadata={meta} />
    {/* Short 9:16 */}
    <Composition id="Story3DShort" component={Story3D} fps={FPS} width={1080} height={1920} durationInFrames={totalFrames(defaults)} defaultProps={defaults} calculateMetadata={meta} />
    {/* YouTube thumbnail */}
    <Still id="Thumbnail" component={Thumbnail} width={1280} height={720} defaultProps={defaults} />
  </>
);
