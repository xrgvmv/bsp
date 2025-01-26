export interface Droneid {
  id: number;
  serial_number: string;
  device_type_id: number;
  device_type: string;
  uuid_len: number;
  uuid: string;
  crc: number;
  unk: number;
  version: number;
  seq_number: number;
  state_info: number;
}
