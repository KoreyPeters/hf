begin
  update public.profiles p
  set points = a.valsum
  from (
    select user_id, SUM(points) valsum
    from public.activities
    where user_id = new.user_id
    group by user_id
  ) a
  where p.id = new.user_id;
  return new;
end;