import { v4 as uuidv4 } from "uuid";
import pluralize from 'pluralize'
import {get, cloneDeep, cloneDeepWith} from 'lodash'

export function toLocal(obj) {
  const { id } = obj;
  const local_id = id ? id: uuidv4();
  return { ...obj, local_id };
}

export function toWriteObjetc(obj) {
  const { local_id, ...rest } = obj;
  let data = {};
  const entries = Object.entries(rest);
  if (entries && entries.length > 0) {
    for (const [key, value] of entries) {
      if (typeof value !== "object") {
        data = { ...data, [key]: value };
        continue;
      }
      if (value.id) {
        data = { ...data, [`${key}_id`]: value.id };
      }
    }
  }
  return data;
}

function objectToForm(obj, formData, prefix=null) {
  const { local_id, ...rest } = obj;
  const entries = Object.entries(rest);
  for (const [key, value] of entries) {
    const flatenKey = prefix ? `${prefix}[${key}]` : key;
    if(Array.isArray(value)){
      value.forEach((item, index) => { 
        if (typeof value[index] !== "object") {
          formData.append(`${flatenKey}[${index}]`, value[index]);
        } else {
          objectToForm(item, formData, `${flatenKey}[${index}]`)
        }
      });
    } else if (value instanceof Blob || typeof value !== "object") {
      formData.append(flatenKey, value);
    } else if (!!value) {
      objectToForm(value, formData, flatenKey)
    }
  }
}

export function toFormData(obj) {
  const formData = new FormData();
  objectToForm(obj,formData);
  return formData;
}

export function getValue(obj, key) {
  key.split(".").forEach(function (item) {
    obj = obj[item];
  });
  return obj;
}

export function getValueByKey(obj, key) {
  let value = null;
  if (key && key.trim().length > 0) {
    const parts = key.split(".");
    let i = 0;
    value = obj[parts[i]];
    while (value && i < parts.length - 1) {
      i++;
      value = value[parts[i]];
    }
  }
  return value;
}

export function overrideFieldIfNullOrEmpty(obj, overrideData) {
  if (!overrideData || !obj) {
    return obj;
  }
  const entries = Object.entries(overrideData);
  if (entries.length === 0) {
    return obj;
  }
  let data = { ...obj };
  entries.forEach(([k,v]) => {
    if (
      !obj[k] || 
      (Array.isArray(obj[k]) && obj[k].length === 0) ||
      (typeof obj[k] ==="object" && Object.entries(obj[k]).length === 0)
    )
    data = { ...data, [k]: v };
  });
  return data;
}

export function clone(obj) {
  // Only handle model field, does not update nested relationship
  let data = {};
  const entries = Object.entries(obj);
  if (entries && entries.length > 0) {
    for (const [key, value] of entries) {
      if (key.endsWith("id") || typeof value !== "object") {
        data = { ...data, [key]: value };
      }
    }
  }
  return data;
}

export function nestedDiff(mine, their, nestedFields=[]) {
  // Compare 2 object and return the diffrent
  const _nestedfields = !nestedFields? [] : nestedFields.map(f => f.split('.')[0]);
  const currentNestedFields = Array.from(new Set(_nestedfields)); // remove duplicate
  //Array
  if (Array.isArray(mine)) {
    if (!Array.isArray(their) || !their) {
      return mine;
    }
    let changes = [];
    let _deletedIDs = their
      .filter((o) => !!o.id && !mine.find((i) => i.id === o.id))
      .map((v) => v.id);
    mine.forEach(((item) => {
      const { id, local_id } = item
      const theirItem = id 
        ? their.find(o => o.id === id)
        : local_id
          ? their.find(o => o.local_id === local_id)
          : null;
      if (!theirItem) {
        changes = [...changes, item]
      } else {
        const diff = nestedDiff(item, theirItem, nestedFields);
        if (diff) {
          changes = [...changes, diff]
        } else if (id) {
          // Keep id to avoid removing item
          changes = [...changes, { id }]
        }
      }
    }));
    const noChange = changes.every((o) => o.id && Object.keys(o).length === 1)
    if (noChange) {
      changes = [];
    }
    if (changes.length > 0 || _deletedIDs.length > 0) {
      return { changes, _deletedIDs}
    }
    return null;
  }
  
  //Object
  if (!mine || typeof mine !== 'object') { //Todo: Review this condition
    return null;
  }
  if (!their) { //Todo: Review this condition
    return mine;
  }
  const mine_keys = mine? Object.keys(mine).filter(
    (key) => key !== "id" && key !== "local_id"
  ) : [];
  const their_keys = their ? Object.keys(their).filter(
    (key) => key !== "id" && key !== "local_id"
  ) : [];
  const keys = [...mine_keys, ...their_keys];
  let data = null;
  keys.forEach(function (key) {
    const mineValue = mine[key];
    const theirValue = their ? their[key] : null;
    if (((!theirValue || theirValue === "") && theirValue !== mineValue) ||
      mineValue instanceof Blob ||
      theirValue instanceof Blob ||
      (mineValue !== theirValue && !Array.isArray(mineValue) && typeof mineValue !== 'object')
    ) {
      data = data ? { ...data, [key]: mineValue } : { [key]: mineValue };
    } else if (mineValue !== theirValue && typeof mineValue === 'object') {
      if (!currentNestedFields.includes(key)) {
        if (mineValue) {
          if (Array.isArray(mineValue)) {
            const myIds = mineValue.filter(o => !!o.id).map(o => o.id);
            const theirIds = theirValue.filter(o => !!o.id).map(o => o.id);
            const theSame = myIds.every((n) => theirIds.includes(n)) &&
              theirIds.every((n) => myIds.includes(n));
            if (!theSame) {
              const foreignKey = `${pluralize.singular(key)}_ids`;
              data = data ? { ...data, [foreignKey]: myIds } : { [foreignKey]: myIds };
            }
          } else {
            const { id: myID } = mineValue;
            const { id: theirID } = theirValue;
            if (myID !== theirID) {
              const foreignKey = `${key}_id`;
              data = data ? { ...data, [foreignKey]: myID } : { [foreignKey]: myID };
            }
          }
        }
      } else {
        const nextNestedFields = nestedFields
          .filter(f => f.startsWith(`${key}.`))
          .map(k => k.split('.').slice(1).join("."));
        const diff = nestedDiff(mineValue, theirValue, nextNestedFields);
        if (diff) {
          if (Array.isArray(mineValue)) {
            const { changes, _deletedIDs } = diff;
            if (changes && changes.length > 0) {
              data = data ? { ...data, [key]: changes } : { [key]: changes };
            }
            if (_deletedIDs && _deletedIDs.length > 0) {
              data = data ? { ...data, [`${key}_deleted_ids`]: _deletedIDs } : { [`${key}_deleted_ids`]: _deletedIDs };
            }
          } else {
            data = data ? { ...data, [key]: diff } : { [key]: diff };
          }
        }
      }
    }
  });
  if (mine.id && data) {
    data = { ...data, id: mine.id };
  }
  return data;
}

function arrayDiff(mine, their) {
  if (!Array.isArray(mine)) {
    return false;
  }
  if (!Array.isArray(their)) {
    return true;
  }
  let changes = [];
  mine.forEach(((item) => {
    if (!their) {
      changes = [...changes, item]
    } else {
      const { id, local_id } = item
      const theirItem = id 
        ? their.find(o => o.id === id)
        : local_id
          ? their.find(o => o.local_id === local_id)
          : null;
      if (!theirItem) {
        changes = [...changes, item]
      }
    }
  }));
  return changes.length > 0;
}

export function diff(mine, their) {
  // Compare 2 object and return the diffrent
  // Just compare their attributes only, it does not take nested compare
  const mine_keys = mine? Object.keys(mine).filter(
    (key) => key !== "id" && key !== "local_id"
  ) : [];
  const their_keys = their ? Object.keys(their).filter(
    (key) => key !== "id" && key !== "local_id"
  ) : [];
  const keys = [...mine_keys, ...their_keys];
  let data = null;
  keys.forEach(function (key) {
    const mineValue = mine ? mine[key] : null;
    const theirValue = their ? their[key]: null;
    if (!their || mineValue !== theirValue) {
      if (arrayDiff(mineValue, theirValue)) {
        data = data ? { ...data, [key]: mineValue } : { [key]: mineValue };
      } else if(mineValue instanceof Blob) {
        data = data ? { ...data, [key]: mineValue } : { [key]: mineValue };
      } else if (mineValue && typeof mineValue === 'object') {
        //Todo:
      } else {
        data = data ? { ...data, [key]: mineValue } : { [key]: mineValue };
      }
    }
  });
  if (mine.id && data) {
    data = { ...data, id: mine.id };
  }
  return data;
}

export function mergeObjects(mine, their, keepKey='mine') {
  if (!keepKey) {
    return {...mine, ...their};
  }
  let _mine = mine ? mine : {};
  const mine_keys = Object.keys(_mine);
  let _their = their ? their : {};
  const their_keys = Object.keys(_their);
  if (keepKey === "mine"){
    _their = Object.entries(_their).reduce((accumulator, entry) => {
      const [k, v] = entry;
      if (mine_keys.includes(k)) {
        const myValue = _mine[k];
        if (v && typeof v === 'object') {
          const value = mergeObjects(myValue, v, keepKey)
          return {...accumulator, [k]: value};
        } else {
          return {...accumulator, [k]: v};
        } 
      } else {
        return accumulator;
      }
    },{});
    return {...mine, ..._their};
  } else {
    _mine = Object.entries(_mine).reduce((accumulator, entry) => {
      const [k, v] = entry;
      if (their_keys.includes(k)) {
        const theirValue = _their[k];
        if (v && typeof v === 'object') {
          const value = mergeObjects(v, theirValue, keepKey)
          return {...accumulator, [k]: value};
        } else {
          return {...accumulator, [k]: v};
        }
      } else {
        return accumulator;
      }
    },{});
    return {..._mine, their};
  }
  
}

export function objectFromDescription(description, parentKey='', referenceObj={}) {
  let obj = {};
  description.forEach((property) => {
    let { name, children, default:defaultValue, type, itemOptions } = property

    if (!name || name.trim().length === 0) {
      return;
    }

    const key = parentKey && parentKey.length > 0
      ? parentKey + "." + name 
      : name;

    if ( type === 'array' && referenceObj && Object.keys(referenceObj).length > 0) {
      if (!itemOptions || itemOptions.length === 0) {
        return;
      }
      children = children | [];
      let propValue = referenceObj ? get(referenceObj, key) : [];
      propValue = propValue ? propValue : [];
      propValue = propValue.filter((v) => !!itemOptions.find((o) => o.name == v.name));
      obj = {...obj, [name]: propValue};
      return;
    }

    if(children) {
      children = objectFromDescription(children, key, referenceObj);
      obj = {...obj, [name]: children}
      return;
    }

    if(defaultValue) {
      obj = {...obj, [name]: defaultValue }
    }
  });
  return obj
}

/***
* Add the key coresponding property key, 
* for example: name1.name11.name111, to the leaf nodes.
* And add item description for array propperties base on referenceObj.
*/
export function normalizeDescription(description, parentKey='', referenceObj={}, toArray=false) {
  let result = [];
  description.forEach((property, i) => {
    let { name, children, default:defaultValue, type, itemOptions } = property;
    if (!name || name.trim().length === 0) {
      return;
    }

    if(toArray) {
      const label = `[${i}]`;
      const key = parentKey && parentKey.length > 0
        ? parentKey + label 
        : label;
      if (children) {
        children = normalizeDescription(property.children, key);
        result = [...result, {...property, children, key, label}];
      }
      return;
    }

    const key = parentKey && parentKey.length > 0
        ? parentKey + "." + name 
        : name;

    if ( type === 'array' && referenceObj && Object.keys(referenceObj).length > 0) {
      if (!itemOptions || itemOptions.length === 0) {
        return;
      }
      children = children | [];
      let propValue = referenceObj ? get(referenceObj, key) : [];
      propValue = propValue ? propValue : [];
      children = propValue
        .map((v, index) => {
          let option = itemOptions.find((o) => o.name == v.name);
          if (!option) {
            return null;
          }
          const label = `[${index}]`;
          return {...option, label, key: `${key}${label}`, children: normalizeDescription(option.children, `${key}${label}`)}
        })
        .filter((o) => !!o);
      result = [...result, {...property, key, children}];
      return;
    }
    
    if (children) {
      children = normalizeDescription(property.children, key);
      result = [...result, {...property, children}];
      return;
    }
    
    result = [...result, {...property, key}];
  });
  return result;
}

/***
* Take an array array and return the new array that elements have been moved into
* children of the other element according on it parent_id attribute.
*/
export function nestedObjects(array=[], parentId=null) {
  let data = [...array];
  let children = parentId
    ? data.filter((o) => o.parent_id == parentId)
    : data.filter((o) => !o.parent_id);

  const children_ids = children.map((o) => o.id);
  data = data.filter((o) => !children_ids.includes(o.id));
  children = children.map((c) => {
    const nestedChildren = nestedObjects(data, c.id);
    return nestedChildren && nestedChildren.length > 0
      ? {...c, children: nestedChildren}
      : c
  });
  return children;
}
