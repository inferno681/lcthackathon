import { ContentModel } from '../../models';
export interface SearchState{
    media: string | null;
    settings: string | null;
    content: ContentModel[];
}

export const initialState: SearchState ={
    media: null,
    settings: null,
    content: []
}