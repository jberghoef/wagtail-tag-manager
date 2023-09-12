export interface WTMWindow extends Window {
  wtm: {
    config_url: string;
    lazy_url: string;
  };
}

export interface Tag {
  name: string;
  attributes: {
    [s: string]: string;
  };
  string: string;
}

export interface Cookie {
  meta: Meta;
  state: {
    [s: string]: string;
  };
}

export interface Meta {
  id?: string;
  set_timestamp?: number;
  refresh_timestamp?: number;
}
